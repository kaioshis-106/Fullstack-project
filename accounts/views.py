from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages  # For feedback messages

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')   # Full Name from form
        username = request.POST.get('username')     # Username
        email = request.POST.get('email')           # Email
        password = request.POST.get('password')     # Password
        confirm_password = request.POST.get('confirm_password')  # Confirm Password

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'signup.html')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name   # store full name in first_name field
        user.save()

        messages.success(request, "Account created successfully! You can log in now.")
        return redirect('login')  # Redirect to login page after signup

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')   # Replace 'main' with your main page url name
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Logs out the current user
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to login page