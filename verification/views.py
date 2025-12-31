from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from time import time
from orders.models import Order
from .utils import verify_qr_signature

QR_EXPIRY_SECONDS = 3600  # 1 hour


@api_view(["POST"])
def verify_qr(request):
    data = request.data

    order_id = data.get("order_id")
    amount = data.get("amount")
    ts = data.get("ts")
    sig = data.get("sig")

    # 1. Basic validation
    if not all([order_id, amount, ts, sig]):
        return Response(
            {"valid": False, "reason": "Missing fields"},
            status=400
        )

    # 2. Expiry check
    now = int(time())
    if now - int(ts) > QR_EXPIRY_SECONDS:
        return Response(
            {"valid": False, "reason": "QR expired"},
            status=400
        )

    # 3. Signature check
    if not verify_qr_signature(order_id, amount, ts, sig):
        return Response(
            {"valid": False, "reason": "Invalid signature"},
            status=400
        )

    # 4–6. Atomic order verification
    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(
                order_id=order_id,
                status="PAID"
            )

            if order.is_verified:
                return Response(
                    {"valid": False, "reason": "QR already used"},
                    status=400
                )

            order.is_verified = True
            order.save()

    except Order.DoesNotExist:
        return Response(
            {"valid": False, "reason": "Order not paid"},
            status=400
        )

    return Response({
        "valid": True,
        "message": "QR verified successfully",
        "order_id": str(order.order_id)
    })
