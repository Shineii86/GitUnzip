"""QR code generation for repo sharing."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def generate_qr(url: str, output_path: str = "repo_qr.png", box_size: int = 10, border: int = 4) -> str:
    """Generate a QR code image. Returns the output path."""
    import qrcode

    qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    logger.info("QR code saved to %s", output_path)
    return output_path


def generate_qr_html(url: str) -> str:
    """Generate an inline QR code as an HTML img tag (base64 encoded)."""
    import qrcode
    import base64
    from io import BytesIO

    qr = qrcode.QRCode(version=1, box_size=8, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<img src="data:image/png;base64,{b64}" width="150" alt="QR Code">'
