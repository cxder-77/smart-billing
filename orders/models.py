import uuid
from django.db import models
from cart.models import Cart

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PAID', 'Paid'),
        ('VERIFIED', 'Verified'),
        ('EXPIRED', 'Expired'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    qr_used = models.BooleanField(default=False)
    qr_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.order_id)
