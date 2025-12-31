from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from orders.models import Order
from .models import Payment


@api_view(["POST"])
def confirm_payment(request):
    order_id = request.data.get("order_id")

    if not order_id:
        return Response({"error": "order_id is required"}, status=400)

    try:
        order = Order.objects.get(order_id=order_id, status="CREATED")
    except Order.DoesNotExist:
        return Response({"error": "Invalid or already paid order"}, status=404)

    payment = Payment.objects.create(
        order=order,
        gateway_payment_id=f"PAY-{order_id}",
        is_verified=True,
        paid_at=timezone.now()
    )

    order.status = "PAID"
    order.save()

    return Response({
        "order_id": str(order.order_id),
        "payment_id": payment.gateway_payment_id,
        "status": order.status
    }, status=status.HTTP_200_OK)
