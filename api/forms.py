from django import forms
from products.models import Product, Category
from comments.models import Comment
from users.models import CustomUser
from cart.models import Cart, CartDetail



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']  # No need to include 'created_by' in the form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'producer', 'description', 'price', 'image', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'user']  # Adjust according to your comment fields

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff']  # Include all necessary fields

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'delivery_address', 'delivery_status', 'delivery_date']

class CartDetailForm(forms.ModelForm):
    class Meta:
        model = CartDetail
        fields = ['product', 'quantity']


