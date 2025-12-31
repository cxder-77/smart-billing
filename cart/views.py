from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer


@api_view(["POST"])
def scan_add_to_cart(request):
    sku = request.data.get("sku")
    cart_id = request.data.get("cart_id")

    if not sku:
        return Response({"error": "SKU is required"}, status=400)

    try:
        product = Product.objects.get(sku=sku, is_active=True)
    except Product.DoesNotExist:
        return Response({"error": "Invalid product"}, status=404)

    if product.stock <= 0:
        return Response({"error": "Out of stock"}, status=400)

    # get or create cart
    if cart_id:
        cart = Cart.objects.get(cart_id=cart_id)
    else:
        cart = Cart.objects.create()

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    serializer = CartItemSerializer(cart.items.all(), many=True)

    return Response({
        "cart_id": str(cart.cart_id),
        "items": serializer.data
    }, status=status.HTTP_200_OK)
