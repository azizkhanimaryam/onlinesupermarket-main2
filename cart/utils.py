# cart/utils.py
from .models import Cart

def get_or_create_cart_for_user(user):
    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        cart.save()
    return cart
