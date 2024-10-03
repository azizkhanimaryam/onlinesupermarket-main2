from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import Category, Product
from cart.models import Cart, CartDetail
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Product
from django.utils import timezone
from products.models import Category, Product
from django.urls import reverse
from django.db import IntegrityError
import logging
from cart.models import Cart, CartDetail, Product
from cart.views import get_or_create_cart_for_user


# Set up logging
logger = logging.getLogger(__name__)


def home(request):
    return render(request=request, template_name="index.html")


def about(request):
    return render(request=request, template_name="about.html")

def rules(request):
    return render(request=request, template_name="rules.html")

def FAQ(request):
    return render(request=request, template_name="FAQ.html")


def contact(request):
    return render(request=request, template_name="contact.html")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ensure the user is authenticated to access cart information
        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
                cart_details = CartDetail.objects.filter(cart=cart)
                total_price = sum(detail.product.price * detail.quantity for detail in cart_details)
                context['cart'] = cart
                context['total_price'] = total_price
            except Cart.DoesNotExist:
                context['cart'] = None
                context['total_price'] = 0  # Default for users without a cart
        else:
            # Handle the case for anonymous users
            context['cart'] = None
            context['total_price'] = 0

        return context



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})



def product_list_by_category(request, category_id):
    if request.user.is_authenticated:
        print(f"Authenticated user: {request.user}")
    else:
        print("User is NOT authenticated")

    # Rest of the code...

    try:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, availability=True)

        logger.info(f"Category: {category}")
        logger.info(f"Products: {products}")

        cart = None
        if request.user.is_authenticated:
            cart = get_or_create_cart_for_user(request.user)  # Fetch or create cart for authenticated users
            logger.info(f"Cart: {cart}")
        else:
            logger.info("User is not authenticated, skipping cart retrieval.")

        context = {
            'category': category,
            'products': products,
            'cart': cart,
        }
        return render(request, 'product_list.html', context)

    except IntegrityError as e:
        logger.error(f"IntegrityError occurred: {e}")
        return HttpResponse("There was an issue accessing this category. Please try again later.")

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []

    return render(request, 'product_search_results.html', {
        'query': query,
        'products': products
    })

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


