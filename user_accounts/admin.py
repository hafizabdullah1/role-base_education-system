import random
import string
from django.core.mail import send_mail
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if obj.pk is None and obj.role == 'teacher':  
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            obj.set_password(password)
            send_mail(
                'Your Account Password',
                f'Your account has been created. Your password is: {password}',
                'your_email@example.com',
                [obj.email],
                fail_silently=False,
            )
        super().save_model(request, obj, form, change)
        
        

admin.site.register(CustomUser, CustomUserAdmin)
