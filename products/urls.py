from django.urls import path
from . import views
from .views import ProductDetailView, ProductListView, product_detail


#app_name = 'products'

urlpatterns = [
    path('index.html', views.home, name="home"),
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('rules.html', views.rules, name="rules"),
    path('FAQ.html', views.FAQ, name="faq"),
    path('contact.html', views.contact, name="contact"),
    path('category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.product_search, name='product_search'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]