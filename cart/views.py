from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from products.models import Product, Category
from .models import Cart, CartDetail
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from django.db import IntegrityError
from api.models import Payment, Order
from cart.models import Cart
import requests
from django.conf import settings

# Create your views here.
from django.db import IntegrityError
import logging


# Set up logging
logger = logging.getLogger(__name__)
def get_or_create_cart_for_user(user):
    if user.is_authenticated:
        try:
            # Fetch the cart for the user, creating one if it doesn't exist
            cart, created = Cart.objects.get_or_create(user=user)
            return cart
        except IntegrityError as e:
            logger.error(f"IntegrityError when fetching or creating cart for user {user}: {e}")
            raise
    else:
        return None  # Return None if the user is not authenticated

@login_required(login_url='users:login')  # Ensure this points to the correct login URL name
def add_to_cart(request, product_id):
    # Fetch the product
    product = get_object_or_404(Product, id=product_id)

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'لطفاً وارد حساب کاربری شوید.')
        return redirect('users:login')

    # Fetch or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    try:
        cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

        # Update the quantity
        if not created:
            cart_detail.quantity += int(request.POST.get('quantity', 1))
        else:
            cart_detail.quantity = int(request.POST.get('quantity', 1))

        cart_detail.save()  # Attempt to save the cart detail

        # Update the total price of the cart
        cart.update_total_price()

        messages.success(request, 'محصول به سبد خرید اضافه شد.')

    except IntegrityError as e:
        messages.error(request, f'خطایی رخ داد: {e}')
        # Optionally log the error for further investigation
        print(f'IntegrityError: {e}')

    return redirect('product_detail', product_id=product_id)



@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user, delivery_status='Pending')
    total_price = cart.total_price  # Retrieve the total price from the cart model
    delivery_price = 5000  # Example fixed delivery price, adjust as needed
    context = {
        'cart': cart,
        'total_price': total_price,  # Pass total_price to the template
        'delivery_price': delivery_price,
    }
    return render(request, 'cart_detail.html', context)

def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, delivery_status='Pending')
    total_price = cart.total_price  # Assuming total_price is updated properly in Cart model
    context = {
        'cart': cart,
        'total_price': total_price  # Pass total_price to the template
    }
    return render(request, 'checkout.html', context)

@login_required
def process_checkout(request):
    if request.method == 'POST':
        # Fetch the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Update quantities
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity < 0:
                        quantity = 0

                    # Attempt to find the cart detail
                    try:
                        cart_detail = CartDetail.objects.get(cart=cart, product_id=product_id)
                        if quantity > 0:
                            cart_detail.quantity = quantity
                            cart_detail.save()
                        else:
                            # Remove the item if quantity is zero
                            cart_detail.delete()
                    except CartDetail.DoesNotExist:
                        messages.error(request, f"Product ID {product_id} was not found in your cart.")
                        return redirect('cart:checkout')

                except ValueError:
                    messages.error(request, f"Invalid quantity for product ID {product_id}.")
                    return redirect('cart:checkout')

        # Process the rest of the checkout details
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        # Create an order (without storing sensitive payment details)
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            zip_code=zip_code,
            country=country,
            total_price=cart.total_price  # Assuming you calculate the total price in your Cart model
        )

        # Now integrate with Zarinpal for the payment
        zarinpal_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
        headers = {'Content-Type': 'application/json'}
        data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': int(cart.total_price) * 10,  # Convert to Toman
            'callback_url': f'{settings.SITE_URL}/api/payment/verify/',
            'description': f'Order {order.id} by {request.user.email}',
            'metadata': {'email': request.user.email}
        }

        response = requests.post(zarinpal_url, json=data, headers=headers)
        response_data = response.json()

        if response_data['data']['code'] == 100:
            # Clear the cart after checkout
            cart.cart_details.all().delete()

            # Redirect the user to Zarinpal payment page
            authority = response_data['data']['authority']
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
        else:
            messages.error(request, "Error processing payment. Please try again.")
            return redirect('cart:checkout')

    return redirect('cart:checkout')

class CartView(ListView):
    model = CartDetail  # Use CartDetail instead of CartItem
    template_name = 'checkout.html'
    context_object_name = 'checkout'

    def get_queryset(self):
        # Get the cart for the current user
        cart = get_object_or_404(Cart, user=self.request.user)
        return CartDetail.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_details = CartDetail.objects.filter(cart=cart)
        total_price = sum(detail.product.price * detail.quantity for detail in cart_details)
        context['total_price'] = total_price
        return context

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'order_confirmation.html', context)

@login_required
def online_payment(request):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    context = {
        'cart': cart,
        'total_price': cart.get_total()  # Assuming there's a method to calculate the total price
    }
    return render(request, 'online_payment.html', context)

@login_required
def process_payment(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        amount = request.POST.get('amount')

        # Create an Order object (without card details, as they are handled via Zarinpal)
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            zip_code=zip_code,
            country=country,
            total_price=amount,
        )

        # After creating the order, integrate with Zarinpal API for payment
        zarinpal_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
        headers = {'Content-Type': 'application/json'}
        data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': int(amount) * 10,  # Convert to Toman
            'callback_url': f'{settings.SITE_URL}/api/payment/verify/',  # Callback URL for payment verification
            'description': f'Order {order.id} by {request.user.email}',
            'metadata': {'email': request.user.email}
        }

        response = requests.post(zarinpal_url, json=data, headers=headers)
        response_data = response.json()

        if response_data['data']['code'] == 100:
            # Redirect the user to Zarinpal payment page
            authority = response_data['data']['authority']
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
        else:
            messages.error(request, "Error processing payment. Please try again.")
            return redirect(reverse('cart:online_payment'))

    return render(request, 'cart/online_payment.html')