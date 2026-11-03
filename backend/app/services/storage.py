"""Small persistence layer: MongoDB when configured, SQLite for local development."""
from __future__ import annotations
import os, sqlite3, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "qr_studio.db"


def _sqlite():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS history (
        id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,
        qr_type TEXT NOT NULL, created_at TEXT NOT NULL, favorite INTEGER NOT NULL DEFAULT 0
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS redirects (
        code TEXT PRIMARY KEY, destination TEXT NOT NULL, created_at TEXT NOT NULL,
        scans INTEGER NOT NULL DEFAULT 0
    )""")
    conn.commit()
    return conn


def _mongo_collection(name: str):
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=1800)
        client.admin.command("ping")
        return client[os.getenv("MONGODB_DATABASE", "qr_code_studio")][name]
    except Exception:
        return None


def add_history(item: dict[str, Any]) -> None:
    col = _mongo_collection("history")
    if col is not None:
        col.update_one({"id": item["id"]}, {"$set": item}, upsert=True)
        return
    with _sqlite() as conn:
        conn.execute("INSERT OR REPLACE INTO history(id,title,content,qr_type,created_at,favorite) VALUES(?,?,?,?,?,?)",
            (item["id"], item["title"], item["content"], item["type"], item["created_at"], int(item.get("favorite", False))))


def list_history() -> list[dict[str, Any]]:
    col = _mongo_collection("history")
    if col is not None:
        return [{k: v for k, v in row.items() if k != "_id"} for row in col.find().sort("created_at", -1).limit(200)]
    with _sqlite() as conn:
        rows = conn.execute("SELECT * FROM history ORDER BY created_at DESC LIMIT 200").fetchall()
    return [{"id": r["id"], "title": r["title"], "content": r["content"], "type": r["qr_type"], "created_at": r["created_at"], "favorite": bool(r["favorite"])} for r in rows]


def delete_history(item_id: str) -> bool:
    col = _mongo_collection("history")
    if col is not None:
        result = col.delete_one({"id": item_id})
        return result.deleted_count > 0
    with _sqlite() as conn:
        cur = conn.execute("DELETE FROM history WHERE id=?", (item_id,))
        return cur.rowcount > 0


def set_favorite(item_id: str, favorite: bool) -> bool:
    col = _mongo_collection("history")
    if col is not None:
        result = col.update_one({"id": item_id}, {"$set": {"favorite": favorite}})
        return result.matched_count > 0
    with _sqlite() as conn:
        cur = conn.execute("UPDATE history SET favorite=? WHERE id=?", (int(favorite), item_id))
        return cur.rowcount > 0


def add_redirect(code: str, destination: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    col = _mongo_collection("redirects")
    if col is not None:
        col.insert_one({"code": code, "destination": destination, "created_at": now, "scans": 0})
        return
    with _sqlite() as conn:
        conn.execute("INSERT INTO redirects(code,destination,created_at,scans) VALUES(?,?,?,0)", (code, destination, now))



def update_redirect(code: str, destination: str) -> bool:
    col = _mongo_collection("redirects")
    if col is not None:
        result = col.update_one({"code": code}, {"$set": {"destination": destination}})
        if result.matched_count:
            _mongo_collection("history").update_one({"id": code}, {"$set": {"content": destination[:2000]}})
        return result.matched_count > 0
    with _sqlite() as conn:
        cur = conn.execute("UPDATE redirects SET destination=? WHERE code=?", (destination, code))
        conn.execute("UPDATE history SET content=? WHERE id=?", (destination[:2000], code))
        return cur.rowcount > 0


def get_redirect(code: str) -> str | None:
    col = _mongo_collection("redirects")
    if col is not None:
        row = col.find_one_and_update({"code": code}, {"$inc": {"scans": 1}})
        return row.get("destination") if row else None
    with _sqlite() as conn:
        row = conn.execute("SELECT destination FROM redirects WHERE code=?", (code,)).fetchone()
        if row:
            conn.execute("UPDATE redirects SET scans=scans+1 WHERE code=?", (code,))
            return row["destination"]
    return None


def analytics() -> dict[str, Any]:
    col = _mongo_collection("history")
    redirects = _mongo_collection("redirects")
    if col is not None:
        return {"total_created": col.count_documents({}), "favorites": col.count_documents({"favorite": True}),
                "dynamic_qr": redirects.count_documents({}) if redirects is not None else 0,
                "total_scans": sum(x.get("scans", 0) for x in redirects.find({}, {"scans": 1})) if redirects is not None else 0}
    with _sqlite() as conn:
        total = conn.execute("SELECT COUNT(*) n FROM history").fetchone()["n"]
        fav = conn.execute("SELECT COUNT(*) n FROM history WHERE favorite=1").fetchone()["n"]
        dyn = conn.execute("SELECT COUNT(*) n FROM redirects").fetchone()["n"]
        scans = conn.execute("SELECT COALESCE(SUM(scans),0) n FROM redirects").fetchone()["n"]
    return {"total_created": total, "favorites": fav, "dynamic_qr": dyn, "total_scans": scans}
