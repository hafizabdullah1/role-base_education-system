from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Count
from user_accounts.models import CustomUser
from education_system.decorators import role_required 

# Create your views here.

# ======================================= Classes Related Views ================================

# Teacher dashboard view
@role_required('teacher')
def dashboard(request):
    classes = Class.objects.annotate(lesson_count=Count('lesson'))
    context = {'classes': classes}
    return render(request, "teacher/dashboard.html", context)



# Create new class view
@role_required('teacher')
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
@role_required('teacher')
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
@role_required('teacher')
def delete_class(request, id):
    my_class = Class.objects.get(id = id)
    print("my_class: ", my_class)
    if request.method == 'POST':
        my_class.delete()
        return redirect("teacher_dashboard")
    context = {'class': my_class}
    return render(request,"teacher/delete_class.html", context)


# ======================================= Lesson Related Views ================================

# Fetch all lessons
@role_required('teacher')
def all_lessons(request):
    lessons = Lesson.objects.annotate(question_count=Count('question'))
    context = {'lessons': lessons}
    return render(request, "teacher/all_lessons.html", context)
    

# fetch Lesson By specific class
@role_required('teacher')
def lesson_by_class(request, id):
    selected_class = Class.objects.get(id=id)
    lessons = Lesson.objects.filter(class_id=selected_class).annotate(question_count=Count('question'))
    # First, filter the lessons associated with the selected class
    # filtered_lessons = Lesson.objects.filter(class_id=selected_class)

    # # Then, filter the questions that are linked to these filtered lessons
    # filtered_questions = Question.objects.filter(lesson_id__in=filtered_lessons)
    context = {'lessons': lessons, 'selected_class': selected_class}
    return render(request, "teacher/lessons_by_class.html", context)


# create new lesson in specific class/course
@role_required('teacher')
def create_lesson_in_class(request, class_id):
    selected_class = Class.objects.get(id=class_id) 

    if request.method == 'POST':
        name = request.POST.get('name')

        try:
            current_teacher = request.user  
            selected_class = Class.objects.get(id=class_id)  

            lesson = Lesson.objects.create(
                name=name,
                class_id=selected_class,
                teacher_id=current_teacher
            )

            lesson.save()

            return redirect("lessons_by_class", id=selected_class.id)

        except Class.DoesNotExist:
            messages.error(request, "The selected class does not exist.")
            return redirect("create_lesson")

    context = {'class': selected_class}
    return render(request, "teacher/create_lesson_in_class.html", context)


# In this creation teacher select the class by drop down to create lesson in which
@role_required('teacher')
def create_lesson(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_class_name = request.POST.get('class')

        try:
            current_teacher = request.user  
            selected_class = Class.objects.get(name=selected_class_name)

            lesson = Lesson.objects.create(
                name=name,
                class_id=selected_class,
                teacher_id=current_teacher
            )

            lesson.save()

            return redirect("lessons_by_class", id=selected_class.id)

        except Class.DoesNotExist:
            messages.error(request, "The selected class does not exist.")
            return redirect("create_lesson")

    context = {'classes': classes}
    return render(request, "teacher/create_lesson.html", context)

@role_required('teacher')
def update_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    classes = Class.objects.all()    
    if request.method == 'POST':

        name = request.POST.get('name')
        selected_class_name = request.POST.get('class')

        selected_class = Class.objects.get(name=selected_class_name)

        lesson.name = name
        lesson.class_id = selected_class
        lesson.save()
        return redirect("lessons_by_class", id=selected_class.id)

    context = {'lesson': lesson, 'classes': classes}
    return render(request, "teacher/update_lesson.html", context)


# delete lesson
@role_required('teacher')
def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id = lesson_id)
    selected_class = lesson.class_id
    if request.method == 'POST':
        lesson.delete()
        return redirect("lessons_by_class", id=selected_class.id)
    context = {'lesson': lesson}
    return render(request,"teacher/delete_lesson.html", context)



# ======================================= Question related views =============================

# fetch questions by specific lesson
@role_required('teacher')
def questoins_by_lesson(request, lesson_id):
    selected_lesson = Lesson.objects.get(id=lesson_id)
    print('selected_lesson: ', selected_lesson)
    questions = Question.objects.filter(lesson_id=selected_lesson)

    question_details = []
    for question in questions:
        if question.type == 'mcqs':
            mcq_answer = Question_MCQS.objects.get(question_id=question)
            question_details.append({
                'type': question.type,
                'statement': question.statement,
                'answer': mcq_answer.answer,
                'id': question.id,
            })
        elif question.type == 'true_false':
            tf_answer = Question_truefalse.objects.get(question_id=question)
            question_details.append({
                'type': question.type,
                'statement': question.statement,
                'answer': tf_answer.answer,
                'id': question.id,

            })
        elif question.type == 'fill_in_blank':
            fb_answer = Question_fillblank.objects.get(question_id=question)
            question_details.append({
                'type': question.type,
                'statement': question.statement,
                'answer': fb_answer.answer,
                'id': question.id,
            })
    
    context = {'questions': question_details, 'lesson': selected_lesson}
    return render(request, "teacher/questions_by_lesson.html", context)


# create question in specific lesson
@role_required('teacher')
def create_question(request, lesson_id):
    if request.method == 'POST':
        lesson = Lesson.objects.get(id=lesson_id)
        statement = request.POST.get('statement')
        question_type = request.POST.get('type')
        
        question = Question.objects.create(
            statement = statement,
            type = question_type,
            lesson_id = lesson
        )
        question.save()
        print("question_type: ", question_type)
        print("statement: ", statement)
        if question_type == 'true_false':
            return redirect("create_true_false_q", question_id=question.id)
        if question_type == 'fill_in_blank':
            return redirect("create_fill_in_blank_q", question_id=question.id)
        if question_type == 'mcqs':
            return redirect("create_mcqs_q", question_id=question.id)
    
    return render(request,"teacher/create_question.html")


# Create true false question
@role_required('teacher')
def create_true_false_q(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':  
        answer = request.POST.get('answer')
        question_true_false = Question_truefalse.objects.create(
            answer = answer,
            question_id = question
        )
        question_true_false.save()
        return redirect("questions_by_lesson", lesson_id=question.lesson_id.id)
        
    context = {'question': question}
    return render(request, "teacher/create_true_false_question.html", context)  


# Create fill_in_blank question
@role_required('teacher')
def create_fill_in_blank_q(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':  
        answer = request.POST.get('answer')
        question_fill_blank = Question_fillblank.objects.create(
            answer = answer,
            question_id = question
        )
        question_fill_blank.save()
        return redirect("questions_by_lesson", lesson_id=question.lesson_id.id)
        
    context = {'question': question}
    return render(request, "teacher/create_fill_the_blank_question.html", context)



# Create mcqs question
@role_required('teacher')
def create_mcqs_q(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':  
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        answer = request.POST.get('answer') 
        
        question_mcqs = Question_MCQS.objects.create(
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            answer=answer,
            question_id=question
        )
        question_mcqs.save()
        return redirect("questions_by_lesson", lesson_id=question.lesson_id.id)
        
    context = {'question': question}
    return render(request, "teacher/create_mcqs_question.html", context)

# Update Specific Question
@role_required('teacher')
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        statement = request.POST.get('statement')
        question.statement = statement
        
        if question.type == 'fill_in_blank':
            answer = request.POST.get('answer')
            fill_blank = get_object_or_404(Question_fillblank, question_id=question)
            fill_blank.answer = answer
            fill_blank.save()
        
        elif question.type == 'true_false':
            answer = request.POST.get('answer')
            true_false = get_object_or_404(Question_truefalse, question_id=question)
            true_false.answer = answer
            true_false.save()
        
        elif question.type == 'mcqs':
            option_a = request.POST.get('option_a')
            option_b = request.POST.get('option_b')
            option_c = request.POST.get('option_c')
            option_d = request.POST.get('option_d')
            answer = request.POST.get('answer')
            mcqs = get_object_or_404(Question_MCQS, question_id=question)
            mcqs.option_a = option_a
            mcqs.option_b = option_b
            mcqs.option_c = option_c
            mcqs.option_d = option_d
            mcqs.answer = answer
            mcqs.save()

        question.save()
        return redirect("questions_by_lesson", lesson_id=question.lesson_id.id)

    else:
        context = {
            'question': {
                'statement': question.statement,
                'type': question.type,
            }
        }

        if question.type == 'mcqs':
            mcqs = get_object_or_404(Question_MCQS, question_id=question)
            context['question']['options'] = {
                'option_a': mcqs.option_a,
                'option_b': mcqs.option_b,
                'option_c': mcqs.option_c,
                'option_d': mcqs.option_d,
            }
            context['question']['answer'] = mcqs.answer

        elif question.type == 'true_false':
            true_false = get_object_or_404(Question_truefalse, question_id=question)
            context['question']['answer'] = true_false.answer

        elif question.type == 'fill_in_blank':
            fill_blank = get_object_or_404(Question_fillblank, question_id=question)
            context['question']['answer'] = fill_blank.answer

        return render(request, "teacher/update_question.html", context)



# Delete question
@role_required('teacher')
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    
    if request.method == 'POST':
        if question.type == 'true_false':
            question_type = Question_truefalse.objects.get(question_id=question_id)
            question_type.delete()
        elif question.type == 'fill_in_blank':
            question_type = Question_fillblank.objects.get(question_id=question_id)
            question_type.delete()
        elif question.type == 'mcqs':
            question_type = Question_MCQS.objects.get(question_id=question_id)
            question_type.delete()
        
        # Finally, delete the main question itself
        question.delete()
        
        # Redirect after deletion
        return redirect("questions_by_lesson", lesson_id=question.lesson_id.id)
    
    # If not POST, show the deletion confirmation page
    context = {'question': question}
    return render(request, "teacher/delete_question.html", context)


# =================================== Student Related views ==========================

# Assigning students to classess
@role_required('teacher')
def assign_students_to_classes(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('student_ids')
        class_id = request.POST.get('class_id') 

        try:
            CustomUser.objects.filter(id__in=user_ids).update(class_id=class_id)
        except Exception as e:
            print(f"Error updating students: {e}")
            
        return redirect('assigned_students')
    
    students = CustomUser.objects.filter(role='student')
    unassigned_students = [std for std in students if not std.class_id or not Class.objects.filter(id=std.class_id.id).exists()]

    classes = Class.objects.all()
    context = {'students': unassigned_students, 'classes': classes}
    return render(request, 'teacher/assign_students_to_classes.html', context)


# List assigned students
@role_required('teacher')
def assigned_students_list(request):
    students = CustomUser.objects.filter(role='student').exclude(class_id=None)
    
    assigned_students = [std for std in students if std.class_id and Class.objects.filter(id=std.class_id.id).exists()]
    
    context = {'students': assigned_students}
    return render(request, "teacher/assigned_students.html", context)


# Remove student from his class
@role_required('teacher')
def remove_assigned_student(request, student_id):
    student = CustomUser.objects.get(id=student_id)
    
    if request.method == 'POST':
        student.class_id = None
        try:
            student.save()
        except Exception as e:
            print(f"Error removing student from class: {e}")
            
        return redirect("assigned_students")

    context = {'student': student}
    return render(request, "teacher/remove_assigned_student.html", context)


# Update assigned student class
@role_required('teacher')
def update_assigned_student(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    
    if request.method == 'POST':
        new_class_id = request.POST.get('class_id')
        try:
            new_class = Class.objects.get(id=new_class_id)
            student.class_id = new_class
            student.save()
            return redirect('assigned_students')
        except Exception as e:
            print(f"Error updating student class: {e}")
    
    classes = Class.objects.all()
    context = {'student': student, 'classes': classes}
    return render(request, "teacher/update_assigned_student.html", context)
