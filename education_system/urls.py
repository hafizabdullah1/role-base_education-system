from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('user_accounts.urls')),
    path('custom_admin/', include('admin_dashboard.urls')),
    path('teacher/', include('teacher.urls')),
]