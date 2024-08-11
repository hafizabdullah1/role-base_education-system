from django.urls import path
from .views import *


urlpatterns = [
    path("", dashboard, name='teacher_dashboard'),
    # Class urls
    path("create_class/", create_class, name='create_class'),
    path("update_class/<int:id>", update_class, name='update_class'),
    path("delete_class/<int:id>", delete_class, name="delete_class"),
    
    # Lesson urls
    path("all_lessons/", all_lessons, name="all_lessons"),
    path("lessons/<int:id>/", lesson_by_class, name="lessons_by_class"),
    path("create_lesson/", create_lesson, name="create_lesson"),
    path("create_lesson/<int:class_id>/", create_lesson_in_class, name="create_lesson"),
    path("update_lesson/<int:lesson_id>/", update_lesson, name="update_lesson"),
    path("delete_lesson/<int:lesson_id>/", delete_lesson, name="delete_lesson"),
    
    # Question urls
    path("questions/<int:lesson_id>/", questoins_by_lesson, name="questions_by_lesson"),
    path("create_question/<int:lesson_id>/", create_question, name="create_question"),
    path("create_true_false_q/<int:question_id>/", create_true_false_q, name="create_true_false_q"),
    path("create_fill_in_blank_q/<int:question_id>/", create_fill_in_blank_q, name="create_fill_in_blank_q"),
    path("create_mcqs_q/<int:question_id>/", create_mcqs_q, name="create_mcqs_q"),
    path("update_question/<int:question_id>/", update_question, name="update_question"),
    path("delete_question/<int:question_id>/", delete_question, name="delete_question"),
    
    # Assing studnets to classes
    path("assign_students/", assign_students_to_classes, name="assign_students"),
    path("assigned_students/", assigned_students_list, name="assigned_students"),
    path("remove_assigned_student/<int:student_id>", remove_assigned_student, name="remove_assigned_student"),
    path("update_assigned_student/<int:student_id>", update_assigned_student, name="update_assigned_student"),
    
    # Result
    path('students_results/<int:class_id>/', students_results, name='students_results'),
    path('student_detailed_results/<int:student_id>/result', student_detailed_results, name='student_detailed_results'),

]