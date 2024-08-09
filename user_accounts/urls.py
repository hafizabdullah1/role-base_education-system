from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path("change_password/", change_password, name="change_password"),


    # Tesing url
    path('student/', student, name='student'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)