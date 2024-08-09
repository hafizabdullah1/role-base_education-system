from django.urls import path
from .views import *


urlpatterns = [
    path("", dashboard, name='teacher_dashboard'),
    path("create_class/", create_class, name='create_class'),
    path("update_class/<int:id>", update_class, name='update_class'),
    path("delete_class/<int:id>", delete_class, name="delete_class"),
    
    # Lesson urls
    path("lessons/<int:id>/", lesson_by_class, name="lessons_by_class"),
    path("create_lesson/", create_lesson, name="create_lesson"),
    path("all_lessons/", all_lessons, name="all_lessons"),
    path("questions/<int:id>", questoins_by_lesson, name="questoins_by_lesson"),
    path("create_question/", create_question, name="create_question"),
    
    # path("create_lesson/", create_lesson, name="create_lesson"),
]