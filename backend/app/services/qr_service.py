from __future__ import annotations
import base64, io, re, uuid
from datetime import datetime, timezone
from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.svg import SvgImage

ERRORS = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}


def build_payload(qr_type: str, data: dict) -> str:
    if qr_type in ("text", "url"):
        value = str(data.get("content", "")).strip()
        if qr_type == "url" and value and not re.match(r"^https?://", value, re.I):
            value = "https://" + value
        return value
    if qr_type == "wifi":
        ssid = str(data.get("ssid", "")).strip()
        password = str(data.get("password", ""))
        security = str(data.get("security", "WPA")).upper()
        if not ssid: raise ValueError("Wi-Fi network name is required.")
        if security not in {"WPA", "WEP", "NOPASS"}: raise ValueError("Unsupported Wi-Fi security type.")
        esc = lambda s: s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\\u003a").replace('"', '\\"')
        return f"WIFI:T:{security};S:{esc(ssid)};P:{esc(password) if security != 'NOPASS' else ''};;"
    if qr_type == "email":
        address = str(data.get("email", "")).strip()
        if not address: raise ValueError("Email address is required.")
        subject = str(data.get("subject", ""))
        body = str(data.get("body", ""))
        from urllib.parse import quote
        return f"mailto:{address}?subject={quote(subject)}&body={quote(body)}"
    if qr_type == "phone":
        phone = str(data.get("phone", "")).strip()
        if not phone: raise ValueError("Phone number is required.")
        return f"tel:{phone}"
    if qr_type == "vcard":
        name = str(data.get("name", "")).strip()
        if not name: raise ValueError("Contact name is required.")
        phone, email, org = (str(data.get(k, "")).strip() for k in ("phone", "email", "organization"))
        return "\n".join(["BEGIN:VCARD", "VERSION:3.0", f"FN:{name}", f"TEL:{phone}" if phone else "", f"EMAIL:{email}" if email else "", f"ORG:{org}" if org else "", "END:VCARD"])
    raise ValueError("Unsupported QR type.")


def create_qr(payload: str, foreground: str="#111827", background: str="#FFFFFF", error: str="M", box_size: int=10, border: int=4, logo: bytes | None=None) -> tuple[bytes, str]:
    if not payload.strip(): raise ValueError("QR content cannot be empty.")
    if error not in ERRORS: raise ValueError("Invalid error correction level.")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", foreground) or not re.fullmatch(r"#[0-9a-fA-F]{6}", background):
        raise ValueError("Colors must be six-digit hexadecimal values.")
    qr = qrcode.QRCode(version=None, error_correction=ERRORS[error], box_size=max(3,min(int(box_size),20)), border=max(4,min(int(border),12)))
    qr.add_data(payload)
    qr.make(fit=True)
    image = qr.make_image(fill_color=foreground, back_color=background).convert("RGB")
    if logo:
        if error != "H":
            raise ValueError("Choose error correction H when embedding a logo for better scan reliability.")
        mark = Image.open(io.BytesIO(logo)).convert("RGBA")
        max_side = int(image.width * 0.19)
        mark.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
        pad = max(6, int(image.width * 0.025))
        plate = Image.new("RGBA", (mark.width + pad*2, mark.height + pad*2), "white")
        plate.alpha_composite(mark, (pad, pad))
        image.paste(plate.convert("RGB"), ((image.width-plate.width)//2, (image.height-plate.height)//2))
    png = io.BytesIO(); image.save(png, format="PNG")
    svg_buffer = io.BytesIO()
    qr.make_image(image_factory=SvgImage, fill_color=foreground, back_color=background).save(svg_buffer)
    return png.getvalue(), svg_buffer.getvalue().decode("utf-8")


def encode_image(data: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
