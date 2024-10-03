from django.db import models
from products.models import Product
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import CustomUser


def get_default_user():
    User = get_user_model()  # This gets the user model defined in settings.AUTH_USER_MODEL
    try:
        return User.objects.get(pk=1).id
    except User.DoesNotExist:
        # Handle the case where the default user does not exist
        return None


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)  # Allow user to be null
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.TextField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(max_length=20, default='Pending')

    def update_total_price(self):
        self.total_price = sum(detail.product.price * detail.quantity for detail in self.cart_details.all())
        print(f"Updated total price: {self.total_price}")  # For debugging purposes
        self.save()

    def __str__(self):
        return f"Cart {self.id} - {self.user.email}"  # Use email instead of username
class CartDetail(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_details')
    quantity = models.IntegerField(default=1)  # Set a default value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total_price()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_total_price()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


