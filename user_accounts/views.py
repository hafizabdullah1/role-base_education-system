import string
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required                
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import urlencode
from django.urls import reverse



# Home page view
def home(request):
    return render(request, "user_accounts/home.html", {})

# Login view
def login_user(request): 
    # This condition will check when user is already login then redirect user to dashboard according to role. 
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect("teacher_dashboard")
        if request.user.role == 'student':
            return redirect("student_dashboard")
        if request.user.is_superuser or user.role == 'admin' :
            return redirect('custom_admin')
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Invalid email")
            return redirect("login")
        
        user = authenticate(username = email, password = password)
                
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login')
        else:
            if user.last_login is None:
                params = urlencode({'user_id': user.id})
                change_password_url = f"{reverse('change_password')}?{params}"
                return redirect(change_password_url)
            else:
                login(request, user)
                if user.role == 'teacher':
                    return redirect("teacher_dashboard")
                if user.role == 'student':
                    return redirect("student_dashboard")
                if user.is_superuser or user.role == 'admin':
                    return redirect('custom_admin')
            
    return render(request, 'user_accounts/login.html')


# Register user view
@user_passes_test(lambda u: u.is_superuser)
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        role = request.POST.get('role')

        user = CustomUser.objects.filter(email = email)
        
        if user.exists():
            messages.info(request, "Email already register.")
            return redirect("register") 
        
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
   
        user = CustomUser.objects.create(
            email = email,
            name = name,
            password = password,
            role = role,
        ) 
        
        user.set_password(password)
        user.save()
                
        subject = 'Welcome to Our Educational Platform'
        html_message = render_to_string('user_accounts/welcome_email.html', {'user': user, 'password': password})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email
        
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return redirect('custom_admin')
    
    return render(request, "user_accounts/register.html", {})
    
# Logout view
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')


# update_user
@login_required(login_url='/login')
def update_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    name = request.POST.get('name')
    email = request.POST.get('email')
    role = request.POST.get('role')

    if request.method == 'POST':
        if user:
            user.name = name
            user.email = email
            user.role = role
            user.save()
            return redirect("custom_admin")

    context = {'form': user}
    
    return render(request, "user_accounts/update_user.html", context)
    
# delete user account from admin dashboard
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, id):
    user = CustomUser.objects.get(id = id)
    if request.method == 'POST':
        user.delete()
        return redirect("custom_admin")
    context = {'user': user}
    return render(request,"user_accounts/delete_user.html", context)    
    

# Change Password
def change_password(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Password and confirm password do not match.")
            return redirect("change_password")
        
        user.set_password(password)
        user.save()
        
        login(request, user)
        
        if user.role == 'teacher':
            return redirect("teacher_dashboard")
        elif user.role == 'student':
            return redirect("student_dashboard")
        elif user.is_superuser or user.role == 'admin':
            return redirect('custom_admin')
    
    return render(request, "user_accounts/change_password.html", {})
