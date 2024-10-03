from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_login, name='login'),  # Updated here
    path('login/', views.user_login, name='login'),  # Updated here
    path('register/', views.register, name='register'),
    path('checklogin/', views.Checklogin, name='checklogin'),
    path('registerAction/', views.registerAction, name='registerAction'),
    #path('checkauth/', views.CheckAuth, name='checkauth'),
    path('logout/', views.LogOut, name='logout'),
    #path('checkloginajaxs/<str:UserName>/<str:Password>/', views.CheckloginAjaxs, name='checkloginajaxs'),
    path('login_ajax/', views.login_ajax, name='login_ajax'),

]
