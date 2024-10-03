from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ProductViewSet, CategoryViewSet, CommentViewSet, UserViewSet,
    PaymentVerifyView, CartViewSet, CategoryListView, CategoryCreateView,
    CategoryEditView, ProductCreateView, ProductEditView, ProductDeleteView, ProductListView,
    CommentCreateView, CommentEditView, CommentListView, UserCreateView,
    UserEditView, UserListView,AdminDashboardView
)

app_name = 'custom_admin'


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)
router.register('cart',viewset=CartViewSet)

cart_list = CartViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

cart_detail = CartViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', include(router.urls)),

    # Products (custom-admin)
    path('custom-admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('custom-admin/products/', ProductListView.as_view(), name='custom-admin-product-list'),
    path('custom-admin/products/create/', ProductCreateView.as_view(), name='custom-admin-product-create'),
    path('custom-admin/products/<int:product_id>/edit/', ProductEditView.as_view(), name='custom-admin-product-edit'),
    path('custom-admin/products/<int:product_id>/delete/', ProductDeleteView.as_view(), name='custom-admin-product-delete'),

    # Categories (custom-admin)
    path('custom-admin/categories/', CategoryListView.as_view(), name='custom-admin-categories-list'),
    path('custom-admin/categories/create/', CategoryCreateView.as_view(), name='custom-admin-category-create'),
    path('custom-admin/categories/<int:category_id>/edit/', CategoryEditView.as_view(), name='custom-admin-category-edit'),

    # Comments (custom-admin)
    path('custom-admin/comments/', CommentListView.as_view(), name='custom-admin-comments-list'),
    path('custom-admin/comments/create/', CommentCreateView.as_view(), name='custom-admin-comment-create'),
    path('custom-admin/comments/<int:comment_id>/edit/', CommentEditView.as_view(), name='custom-admin-comment-edit'),

    # Users (custom-admin)
    path('custom-admin/users/', UserListView.as_view(), name='custom-admin-users-list'),
    path('custom-admin/users/create/', UserCreateView.as_view(), name='custom-admin-user-create'),
    path('custom-admin/users/<int:user_id>/edit/', UserEditView.as_view(), name='custom-admin-user-edit'),

    # Payments
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment_verify'),

    # Carts (custom-admin)
    path('custom-admin/carts/', cart_list, name='custom-admin-cart-list'),
    path('custom-admin/carts/<int:pk>/', cart_detail, name='custom-admin-cart-detail'),
    path('custom-admin/carts/<int:pk>/details/', CartViewSet.as_view({'get': 'get_cart_details'}), name='custom-admin-cart-details'),
]