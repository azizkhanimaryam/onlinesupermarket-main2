from django.urls import path
from . import views
from .views import add_to_cart,checkout,CartView


app_name = 'cart'  # Ensure this line is present

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process/', views.process_checkout, name='process_checkout'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('detail/', views.cart_detail, name='cart_detail'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('online-payment/', views.online_payment, name='online_payment'),  # Ensure this URL pattern is defined
]




