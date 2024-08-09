from django.urls import path
from .views import *


urlpatterns = [
    path("", dashboard, name='custom_admin'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]