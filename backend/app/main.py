from __future__ import annotations
import base64, csv, io, os, re, secrets, zipfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse, Response
from pydantic import BaseModel, Field
import cv2, numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .services.qr_service import build_payload, create_qr, encode_image, new_id, timestamp
from .services import storage

app = FastAPI(title="QR Code Studio API", version="1.0.0", description="QR generation, scanning, history, bulk export and dynamic redirects.")
origins = [x.strip() for x in os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class GenerateRequest(BaseModel):
    type: str = "text"
    data: dict = Field(default_factory=dict)
    title: str = "Untitled QR"
    foreground: str = "#111827"
    background: str = "#FFFFFF"
    error_correction: str = "M"
    box_size: int = 10
    border: int = 4
    logo_base64: str | None = None

class FavoriteRequest(BaseModel):
    favorite: bool

class DynamicRequest(BaseModel):
    destination: str
    title: str = "Dynamic QR"

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "QR Code Studio API"}

@app.post("/api/qr/generate")
async def generate(body: GenerateRequest):
    try:
        payload = build_payload(body.type, body.data)
        logo_bytes = base64.b64decode(body.logo_base64) if body.logo_base64 else None
        png, svg = create_qr(payload, body.foreground, body.background, body.error_correction, body.box_size, body.border, logo_bytes)
        item_id = new_id()
        item = {"id": item_id, "title": body.title[:100], "content": payload[:2000], "type": body.type, "created_at": timestamp(), "favorite": False}
        storage.add_history(item)
        return {"id": item_id, "title": item["title"], "payload": payload, "png": encode_image(png), "svg": svg, "created_at": item["created_at"]}
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        raise HTTPException(500, f"QR generation failed: {exc}")

@app.post("/api/qr/scan")
async def scan(file: UploadFile = File(...)):
    raw = await file.read()
    if len(raw) > 12 * 1024 * 1024: raise HTTPException(413, "Image must be smaller than 12 MB.")
    arr = np.frombuffer(raw, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None: raise HTTPException(400, "The uploaded file is not a supported image.")
    detector = cv2.QRCodeDetector()
    decoded, points, _ = detector.detectAndDecode(image)
    if not decoded: raise HTTPException(422, "No readable QR code was detected.")
    return {"content": decoded, "is_url": decoded.lower().startswith(("https://", "http://"))}

@app.get("/api/history")
def history():
    return {"items": storage.list_history()}

@app.delete("/api/history/{item_id}")
def remove_history(item_id: str):
    if not storage.delete_history(item_id): raise HTTPException(404, "QR record not found.")
    return {"deleted": True}

@app.patch("/api/history/{item_id}/favorite")
def favorite(item_id: str, body: FavoriteRequest):
    if not storage.set_favorite(item_id, body.favorite): raise HTTPException(404, "QR record not found.")
    return {"updated": True, "favorite": body.favorite}

@app.get("/api/analytics")
def analytics():
    return storage.analytics()

@app.post("/api/qr/dynamic")
def create_dynamic(body: DynamicRequest):
    destination = body.destination.strip()
    if not re.match(r"^https?://", destination, re.I): raise HTTPException(400, "Destination must start with http:// or https://")
    code = secrets.token_urlsafe(7).replace("-", "").replace("_", "")[:10]
    storage.add_redirect(code, destination)
    storage.add_history({"id": code, "title": body.title[:100], "content": destination[:2000], "type": "dynamic", "created_at": timestamp(), "favorite": False})
    base = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000").rstrip("/")
    url = f"{base}/r/{code}"
    png, svg = create_qr(url)
    return {"code": code, "url": url, "png": encode_image(png), "svg": svg}

@app.patch("/api/qr/dynamic/{code}")
def update_dynamic(code: str, body: DynamicRequest):
    destination = body.destination.strip()
    if not re.match(r"^https?://", destination, re.I): raise HTTPException(400, "Destination must start with http:// or https://")
    if not storage.update_redirect(code, destination): raise HTTPException(404, "Dynamic QR link not found.")
    base = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000").rstrip("/")
    return {"code": code, "url": f"{base}/r/{code}", "destination": destination, "updated": True}

@app.get("/r/{code}")
def redirect_dynamic(code: str):
    destination = storage.get_redirect(code)
    if not destination: raise HTTPException(404, "This dynamic QR link does not exist.")
    return RedirectResponse(destination, status_code=307)

@app.post("/api/bulk")
async def bulk(file: UploadFile = File(...), content_column: str = Form("content")):
    raw = await file.read()
    if len(raw) > 5 * 1024 * 1024: raise HTTPException(413, "CSV must be smaller than 5 MB.")
    try:
        text = raw.decode("utf-8-sig")
        rows = list(csv.DictReader(io.StringIO(text)))
    except Exception: raise HTTPException(400, "Could not read CSV. Save it as UTF-8 CSV and try again.")
    if not rows: raise HTTPException(400, "CSV has no data rows.")
    if content_column not in (rows[0] or {}): raise HTTPException(400, f"Column '{content_column}' was not found.")
    if len(rows) > 500: raise HTTPException(400, "Maximum 500 QR codes per batch.")
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        for index, row in enumerate(rows, 1):
            value = str(row.get(content_column, "")).strip()
            if not value: continue
            png, _ = create_qr(value)
            archive.writestr(f"qr-{index:03d}.png", png)
    memory.seek(0)
    return StreamingResponse(memory, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=qr-code-batch.zip"})

@app.post("/api/qr/pdf")
async def export_pdf(file: UploadFile = File(...)):
    raw = await file.read()
    if len(raw) > 12 * 1024 * 1024: raise HTTPException(413, "Image is too large.")
    image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    if image is None: raise HTTPException(400, "Invalid image.")
    ok, encoded = cv2.imencode(".png", image)
    if not ok: raise HTTPException(500, "Could not process image.")
    pdf = io.BytesIO(); page = canvas.Canvas(pdf, pagesize=(420, 480))
    page.setFont("Helvetica-Bold", 18); page.drawString(36, 438, "QR Code Studio")
    page.drawImage(ImageReader(io.BytesIO(encoded.tobytes())), 70, 90, 280, 280, preserveAspectRatio=True, anchor="c")
    page.setFont("Helvetica", 9); page.drawString(36, 45, "Generated with QR Code Studio")
    page.save(); pdf.seek(0)
    return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=qr-code.pdf"})
