from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            name = user.username  # get username

            # ROLE-BASED GREETING
            if user.is_superuser:
                messages.success(request, f"👑 Welcome Admin {name}! You have successfully logged in.")
            elif hasattr(user, 'userprofile') and user.userprofile.role == 'staff':
                messages.success(request, f"🛠️ Welcome Staff {name}! You have successfully logged in.")
            else:
                messages.success(request, f"👤 Welcome User {name}! You have successfully logged in.")

            return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')