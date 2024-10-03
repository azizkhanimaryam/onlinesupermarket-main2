from django.contrib import admin
from .models import Cart, CartDetail

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'delivery_status')
    search_fields = ('user__email',)

@admin.register(CartDetail)
class CartDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_filter = ('cart', 'product')



