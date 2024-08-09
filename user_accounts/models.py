from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import MyAccountManager

# Create your models here.


class CustomUser(AbstractUser):
    username                = None
    name                    = models.CharField(max_length=255)
    email                   = models.EmailField(max_length=255, unique=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.name


















# class CustomUser(AbstractUser):
#     email                    = models.EmailField(verbose_name='email', max_length=60, unique=True)
#     name                     = models.CharField(verbose_name='name', max_length=255)
#     date_joined              = models.DateTimeField(verbose_name='date joined', auto_now_add=True)    
#     last_login               = models.DateTimeField(verbose_name='last login', auto_now=True)    
#     is_superuser             = models.BooleanField(default=False)
#     profile_image            = models.ImageField(max_length=255, upload_to="images/", null=True, blank=True, default="")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']
    
#     objects = MyAccountManager()
    
#     def __str__(self):
#         self.name



# class CustomUser(AbstractUser):
#     username = None 
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
    
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student')
#     ]
    
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.name