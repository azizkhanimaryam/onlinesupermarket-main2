"""
URL configuration for supermarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from products.views import home
from api.views import (
    ProductListView, ProductCreateView, ProductEditView,
    CategoryListView, CategoryCreateView, CategoryEditView,
    CommentListView, CommentCreateView, CommentEditView,
    UserListView, UserCreateView, UserEditView,
    cart_list, cart_detail, cart_edit
)


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('custom-admin/', include('api.urls')),
    #path('custom-admin/products/', ProductListView.as_view(), name='admin-products-list'),
    #path('custom-admin/products/create/', ProductCreateView.as_view(), name='admin-product-create'),
    #path('custom-admin/products/<int:product_id>/edit/', ProductEditView.as_view(), name='admin-product-edit'),  # Edit product URL
    # Category paths
    #path('custom-admin/categories/', CategoryListView.as_view(), name='admin-categories-list'),
    #path('custom-admin/categories/<int:category_id>/edit/', CategoryEditView.as_view(), name='admin-category-edit'),

    # Comment paths
    #path('custom-admin/comments/', CommentListView.as_view(), name='admin-comments-list'),
    #path('custom-admin/comments/create/', CommentCreateView.as_view(), name='admin-comment-create'),
    #path('custom-admin/comments/<int:comment_id>/edit/', CommentEditView.as_view(), name='admin-comment-edit'),

    # User paths
    #path('custom-admin/users/', UserListView.as_view(), name='admin-users-list'),
    #path('custom-admin/users/create/', UserCreateView.as_view(), name='admin-user-create'),
    #path('custom-admin/users/<int:user_id>/edit/', UserEditView.as_view(), name='admin-user-edit'),

    # Cart paths
    #path('custom-admin/carts/', cart_list, name='admin-cart-list'),
    #path('custom-admin/carts/<int:cart_id>/', cart_detail, name='admin-cart-detail'),
    #path('custom-admin/carts/<int:cart_id>/edit/', cart_edit, name='admin-cart-edit'),

    path('', include("products.urls")),
    #path('products/', include('products.urls', namespace='products')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include('cart.urls')),  # Include cart app URLs
    path('comments/', include('comments.urls')),
    path('users/', include('users.urls',namespace='users')),
    path('', home, name='home'),  # Add this line to define the 'home' URL pattern
    path('__debug__/', include('debug_toolbar.urls')),  # Include this line
    path('api/',include('api.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

