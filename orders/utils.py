import json
import hmac
import hashlib
import time
from django.conf import settings
import qrcode
import json
from io import BytesIO


def generate_master_qr_payload(order_id, amount):
    timestamp = int(time.time())

    payload = {
        "order_id": str(order_id),
        "amount": float(amount),
        "ts": timestamp
    }

    message = json.dumps(payload, sort_keys=True).encode()
    secret = settings.QR_SECRET_KEY.encode()

    signature = hmac.new(secret, message, hashlib.sha256).hexdigest()

    payload["sig"] = signature
    return payload

def generate_qr_image(payload: dict):
    """
    Takes QR payload (dict) and returns PNG image bytes
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qr.add_data(json.dumps(payload))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer