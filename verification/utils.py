import json
import hmac
import hashlib
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def verify_qr_signature(order_id, amount, ts, received_sig):
    if not hasattr(settings, "QR_SECRET_KEY"):
        raise ImproperlyConfigured("QR_SECRET_KEY is not set")

    payload = {
        "order_id": str(order_id),
        "amount": float(amount),
        "ts": int(ts)
    }

    message = json.dumps(payload, sort_keys=True).encode()
    secret = settings.QR_SECRET_KEY.encode()

    expected_sig = hmac.new(
        secret,
        message,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_sig, received_sig)
