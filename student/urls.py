from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name='student_dashboard'),
    path("questions/<int:lesson_id>/", questions, name='questions'),
    path("quizing/<int:lesson_id>/", quizing, name='quizing'),
]