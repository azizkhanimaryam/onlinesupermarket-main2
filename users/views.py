from django.shortcuts import render, redirect
from .forms import Login, Register
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login as auth_login



def user_login(request):
    form = Login()
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Use email for authentication
            if user is not None:
                login(request, user)
                request.session.save()  # Explicitly save the session
                return redirect('home')  # Adjust this redirect as necessary
            else:
                return HttpResponse("حسابی با این مشخصات یافت نشد")
    return render(request, "login.html", {"form": form})

def login_ajax(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



# views.py

def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return HttpResponse("این کاربر قبلا در سیستم ثبت نام شده است.")
            else:
                # Save the new user
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                auth_login(request, user)  # Use the correct login function
                return HttpResponse("حساب کاربری ساخته شد")
        else:
            # Print form errors for debugging
            print(f"Form errors: {form.errors}")
            return render(request, "register.html", {"form": form, "errors": form.errors})

    return render(request, "register.html", {"form": form})




def registerAction(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                return HttpResponse("این کاربر قبلا در سیستم ثبت نام شده است.")
            else:
                user = form.save()
                return render(request, "registration_success.html", {"form": form})
        else:
            return render(request, "register.html", {"form": form, "errors": form.errors})
    else:
        form = Register()
    return render(request, "register.html", {"form": form})

def LogOut(request):
    logout(request)
    return redirect('home')

def Checklogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated successfully, log them in
            login(request, user)
            # Redirect to a success page
            return redirect('home')  # Adjust to your home or target page
        else:
            # If authentication fails, send a message and reload the login page
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
            return redirect('users:login')  # Redirect back to login page

    # Handle GET or any unexpected method by redirecting to the login page
    return redirect('users:login')

