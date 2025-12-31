from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart
from .models import Order

from .utils import generate_master_qr_payload


@api_view(["POST"])
def create_order(request):
    cart_id = request.data.get("cart_id")

    if not cart_id:
        return Response({"error": "cart_id is required"}, status=400)

    try:
        cart = Cart.objects.get(cart_id=cart_id, is_active=True)
    except Cart.DoesNotExist:
        return Response({"error": "Invalid cart"}, status=404)

    total = 0
    for item in cart.items.all():
        total += item.product.price * item.quantity

    order = Order.objects.create(
        cart=cart,
        total_amount=total,
        status="CREATED"
    )

    cart.is_active = False
    cart.save()

    return Response({
        "order_id": str(order.order_id),
        "total_amount": total,
        "status": order.status
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def generate_master_qr(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, status="PAID")
    except Order.DoesNotExist:
        return Response({"error": "Invalid or unpaid order"}, status=404)

    qr_payload = generate_master_qr_payload(
        order.order_id,
        order.total_amount
    )

    return Response(qr_payload, status=200)