from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login                 
from django.contrib import messages


# Create your views here.


def home(request):
    return render(request, "home.html", {})

def loginView(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Invalid email")
            print("email error")
            return redirect("login")
        
        user = authenticate(username = email, password = password)
        
        print("user:", user)
        
        if user is None:
            messages.error(request, "Invalid password")
            print("password error")
            return redirect('login')
        else:
            login(request, user)

            user = CustomUser.objects.get(email=email)

            if user.role == 'teacher':
                return redirect("teacher")

            if user.role == 'student':
                return redirect("student")
            if user.role == 'admin':
                return redirect('admin')
            
    return render(request, 'login.html')


# Techer dahsboard
def teacher(request):
    return render(request,"teacher.html")


def student(request):
    return render(request,"student.html")
