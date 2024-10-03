from django.contrib import admin,messages
from .models import Category, Product, Stock
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages

def check_integrity(modeladmin, request, queryset):
    try:
        for obj in queryset:
            # Example check: Stock's category must match the product's category
            if isinstance(obj, Stock) and obj.category != obj.product.category:
                raise IntegrityError("Stock's category must match the product's category.")
    except IntegrityError as e:
        modeladmin.message_user(request, f"Integrity check failed: {e}", level='error')


check_integrity.short_description = "Check integrity of selected items"

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'created_by')
    search_fields = ('name',)

    # Automatically set created_by to the current user
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'created_by')
    search_fields = ('name',)
    list_filter = ('category',)
    actions = [check_integrity]

    # Automatically set created_by to the current user
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Register the Stock model
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'quantity')
    list_filter = ('category',)
    search_fields = ('product__name',)
    actions = [check_integrity]

    def save_model(self, request, obj, form, change):
        if obj.product.category != obj.category:
            messages.error(request, "The category of the stock must match the product's category.")
            raise ValidationError("The category of the stock must match the product's category.")
        super().save_model(request, obj, form, change)


# Register the MostSoldProduct model
