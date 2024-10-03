from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from api.models import Payment, Order
from cart.models import Cart
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from api.serializers import CartSerializer
import requests
from django.conf import settings
from products.models import Product, Category
from comments.models import Comment
from users.models import CustomUser
from products.serializers import ProductSerializer, CategorySerializer
from comments.serializers import CommentSerializer
from users.serializers import CustomUserSerializer
from cart.serializers import CartSerializer
from .forms import ProductForm, CategoryForm,  CommentForm, UserForm
from cart.models import Cart
from .forms import CartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q
from products.models import Product, Category
from comments.models import Comment
from cart.models import Cart
from users.models import CustomUser
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')

        # Filter products
        context['product_list'] = Product.objects.filter(name__icontains=search_query) if search_query else Product.objects.all()
        # Filter categories
        context['category_list'] = Category.objects.filter(name__icontains=search_query) if search_query else Category.objects.all()
        # Filter comments
        context['comment_list'] = Comment.objects.filter(content__icontains=search_query) if search_query else Comment.objects.all()
        # Filter users
        context['user_list'] = CustomUser.objects.filter(email__icontains=search_query) if search_query else CustomUser.objects.all()
        # Filter carts (based on whatever fields you want)
        context['cart_list'] = Cart.objects.filter(delivery_address__icontains=search_query) if search_query else Cart.objects.all()

        return context



class PaymentVerifyView(APIView):
    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        payment = get_object_or_404(Payment, authority=authority)

        if status == 'OK':
            # Verify the payment with Zarinpal
            verify_url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
            headers = {'Content-Type': 'application/json'}
            data = {
                'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                'authority': authority,
                'amount': int(payment.amount * 10),  # Amount in Toman
            }

            response = requests.post(verify_url, json=data, headers=headers)
            response_data = response.json()

            if response_data['data']['code'] == 100:
                # Payment was successful
                payment.is_paid = True
                payment.paid_at = timezone.now()
                payment.save()

                # Deactivate the cart or perform any other post-payment actions
                payment.cart.is_active = False
                payment.cart.save()

                # Return success response with RefID
                return Response({'message': 'Payment successful', 'ref_id': response_data['data']['ref_id']})
            else:
                # Payment verification failed
                return Response({'error': response_data['errors']}, status=400)
        else:
            # Payment was not successful
            return Response({'message': 'Payment was not successful'}, status=400)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_cart_details(self, request, pk=None):
        cart = self.get_object()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# ViewSet for Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSet for Comments
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# ViewSet for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@method_decorator(staff_member_required, name='dispatch')
class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'custom-admin/categories_list.html', {'categories': categories})

# Create category
@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'admin/category_form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user  # Set the created_by field to the logged-in user
            category.save()
            return redirect('admin-categories-list')  # Redirect to the category list
        return render(request, 'admin/category_form.html', {'form': form})

# Edit category
@method_decorator(staff_member_required, name='dispatch')
class CategoryEditView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        return render(request, 'admin/category_form.html', {'form': form})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user  # Update the creator to the logged-in user
            category.save()
            return redirect('admin-categories-list')  # Redirect to the category list
        return render(request, 'admin/category_form.html', {'form': form})
@method_decorator(login_required, name='dispatch')
class ProductListView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        query = request.GET.get('q', '')
        products = Product.objects.filter(name__icontains=query)  # Search functionality
        return render(request, 'admin/products_list.html', {'products': products})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin/product_form.html'
    success_url = reverse_lazy('custom-admin-product-list')

# Product Edit View
class ProductEditView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(instance=product)
        return render(request, 'admin/product_form.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('custom-admin-product-list')  # Redirect to product list after saving
        return render(request, 'admin/product_form.html', {'form': form, 'product': product})

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin-dashboard')  # Redirect to dashboard after deletion


# Create comment
@method_decorator(staff_member_required, name='dispatch')
class CommentCreateView(View):
    def get(self, request):
        form = CommentForm()
        return render(request, 'admin/comment_form.html', {'form': form})

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-comments-list')  # Redirect to the comment list
        return render(request, 'admin/comment_form.html', {'form': form})

# Edit comment
@method_decorator(staff_member_required, name='dispatch')
class CommentEditView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(instance=comment)
        return render(request, 'admin/comment_form.html', {'form': form})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('admin-comments-list')  # Redirect to the comment list
        return render(request, 'admin/comment_form.html', {'form': form})

class CommentListView(View):
    def get(self, request):
        comments = Comment.objects.all()
        return render(request, 'admin/comments_list.html', {'comments': comments})

# Create user
@method_decorator(staff_member_required, name='dispatch')
class UserCreateView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'admin/user_form.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-users-list')  # Redirect to the user list
        return render(request, 'admin/user_form.html', {'form': form})

# Edit user
@method_decorator(staff_member_required, name='dispatch')
class UserEditView(View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = UserForm(instance=user)
        return render(request, 'admin/user_form.html', {'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin-users-list')  # Redirect to the user list
        return render(request, 'admin/user_form.html', {'form': form})
class UserListView(View):
    def get(self, request):
        users = CustomUser.objects.all()
        return render(request, 'admin/users_list.html', {'users': users})

# List of all carts
@staff_member_required  # Ensure only staff can access
def cart_list(request):
    carts = Cart.objects.all()
    return render(request, 'admin_panel/cart_list.html', {'carts': carts})

# View cart details
@staff_member_required  # Ensure only staff can access
def cart_detail(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    return render(request, 'admin_panel/cart_details.html', {'cart': cart})

# Edit cart (e.g., update delivery status)
@staff_member_required  # Ensure only staff can access
def cart_edit(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect('cart_list')
    else:
        form = CartForm(instance=cart)
    return render(request, 'admin_panel/cart_edit.html', {'form': form, 'cart': cart})