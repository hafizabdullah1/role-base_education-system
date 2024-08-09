from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

# ============== Class Related Views =================

# Teacher dashboard view
@login_required(login_url='/login')
def dashboard(request):
    classes = Class.objects.all()
    context = {'classes': classes}
    return render(request, "teacher/dashboard.html", context)


# Create new class view
@login_required(login_url='/login')
def create_class(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        new_class = Class.objects.filter(name = name)
        
        if new_class.exists():
            messages.info(request, "Class already register.")
            return redirect('create_class')

        new_class = Class.objects.create(name=name, teacher_id = request.user)
        new_class.save()
        return redirect("teacher_dashboard")
    
    return render(request, "teacher/create_class.html", {})


# Update class view
@login_required(login_url='/login')
def update_class(request, id):
    get_class = get_object_or_404(Class, id=id)
    name = request.POST.get('name')
    if request.method == 'POST':
        if get_class:
            get_class.name = name
            get_class.save()
            return redirect("teacher_dashboard")

    context = {'form': get_class}
    
    return render(request, "teacher/update_class.html", context)


# Delete class view
@login_required(login_url='/login')
def delete_class(request, id):
    my_class = Class.objects.get(id = id)
    if request.method == 'POST':
        my_class.delete()
        return redirect("teacher_dashboard")
    context = {'class': my_class}
    return render(request,"teacher/delete_class.html", context)


# ============== Lesson Related Views =================



# fetch Lesson By specific class
@login_required(login_url='/login')
def lesson_by_class(request, id):
    selected_class = Class.objects.get(id=id)
    lessons = Lesson.objects.filter(class_id=selected_class)
    context = {'lessons': lessons}
    return render(request, "teacher/lessons_by_class.html", context)


# create new lesson in specific class/course
@login_required(login_url='/login')
def create_lesson(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        selected_class_name = request.POST.get('class')

        try:
            # Retrieve the Class instance using get()
            selected_class = Class.objects.get(name=selected_class_name)
            current_teacher = request.user  # Assuming the logged-in user is the teacher


            # Create the Lesson and assign the Class instance to class_id
            lesson = Lesson.objects.create(
                name=name,
                class_id=selected_class,
                teacher_id = current_teacher
            )

            return redirect("lessons_by_class", id=selected_class.id)

        except Class.DoesNotExist:
            # Handle the case where the class does not exist
            messages.error(request, "The selected class does not exist.")
            return redirect("create_lesson")

    return render(request, "teacher/create_lesson.html", {'classes': classes})


# Fetch all lessons
@login_required(login_url="/")
def all_lessons(request):
    lessons = Lesson.objects.all()
    context = {'lessons': lessons}
    return render(request, "teacher/all_lessons.html", context)
    

# fetch questions by specific lesson
@login_required(login_url="/")
def questoins_by_lesson(request, id):
    selected_lesson = Lesson.objects.get(id=id)
    questions = Question.objects.filter(lesson_id=selected_lesson)
    context = {'questions': questions}
    return render(request, "teacher/questions_by_class.html", context)


# create question in specific lesson
@login_required(login_url="/")
def create_question(request):
    if request.method == 'POST':
        statement = request.POST.get('statement')
        question_type = request.POST.get('type')
        
        print("Statement: ", statement)
        print("Type: ", question_type)
    
    context = {}
    return render(request,"teacher/create_question.html", context)



# # Create new class view
# @login_required(login_url='/login')
# def create_class(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
        
#         new_class = Class.objects.filter(name = name)
        
#         if new_class.exists():
#             messages.info(request, "Class already register.")
#             return redirect('create_class')

#         new_class = Class.objects.create(name=name, teacher_id = request.user)
#         new_class.save()
#         return redirect("teacher_dashboard")
    
#     return render(request, "teacher/create_class.html", {})


# # Update class view
# @login_required(login_url='/login')
# def update_class(request, id):
#     get_class = get_object_or_404(Class, id=id)
#     name = request.POST.get('name')
#     if request.method == 'POST':
#         if get_class:
#             get_class.name = name
#             get_class.save()
#             return redirect("teacher_dashboard")

#     context = {'form': get_class}
    
#     return render(request, "teacher/update_class.html", context)


# # Delete class view
# @login_required(login_url='/login')
# def delete_class(request, id):
#     my_class = Class.objects.get(id = id)
#     if request.method == 'POST':
#         my_class.delete()
#         return redirect("teacher_dashboard")
#     context = {'class': my_class}
#     return render(request,"teacher/delete_class.html", context)


# # ============== Lesson Related Views =================
