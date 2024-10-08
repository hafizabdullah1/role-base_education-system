from django.shortcuts import render, redirect, get_object_or_404
from education_system.decorators import role_required
from teacher.models import *
from django.http import JsonResponse
from django.db.models import Sum
import logging
from django.contrib import messages

# Dashboard with all lessons list of his class

@role_required('student')
def dashboard(request):
    student = request.user
    student_class = student.class_id
    lessons = []
    
    if student_class is not None:
        lessons = Lesson.objects.filter(class_id=student_class)
        
        for lesson in lessons:
            all_questions = Question.objects.filter(lesson_id=lesson).values_list('id', flat=True)
            
            attempted_questions = Result.objects.filter(
                student_id=student,
                question_id__lesson_id=lesson,
            ).values_list('question_id', flat=True)

            attempted_questions_set = set(attempted_questions)
            
            total_questions_count = len(all_questions)
            attempted_count = sum(1 for q_id in all_questions if q_id in attempted_questions_set)
            non_attempted_count = total_questions_count - attempted_count
            
            lesson.question_count = total_questions_count
            lesson.attempted_count = attempted_count
            lesson.non_attempted_count = non_attempted_count

    context = {'lessons': lessons, 'student': request.user}
    return render(request, "student/dashboard.html", context)


# Question of lessons
@role_required('student')
def questions(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    student = request.user
    questions = Question.objects.filter(lesson_id=lesson_id)

    attempted_questions = set(
        Result.objects.filter(student_id=student, question_id__lesson_id=lesson).values_list('question_id', flat=True)
    )
    
    questions_with_attempt_status = []
    for question in questions:
        question_data = {
            'statement': question.statement,
            'type': question.type,
            'attempted': question.id in attempted_questions,
        }
        questions_with_attempt_status.append(question_data)

    context = {'questions': questions_with_attempt_status, 'lesson': lesson}
    return render(request, "student/questions.html", context)



# Start quizing according to selected lesson
logger = logging.getLogger(__name__)

# Configure logger
@role_required('student')
def quizing(request, lesson_id):
    student = request.user
    lesson = Lesson.objects.get(id=lesson_id)
    questions = Question.objects.filter(lesson_id=lesson)

    attempted_questions = Result.objects.filter(student_id=student, question_id__lesson_id=lesson).values_list('question_id', flat=True)

    questions_with_options = []
    for question in questions:
        if question.id not in attempted_questions:
            question_data = {
                'id': question.id,
                'statement': question.statement,
                'type': question.type,
            }
            
            if question.type == 'mcqs':
                try:
                    mcqs = Question_MCQS.objects.get(question_id=question)
                    question_data['options'] = {
                        'option_a': mcqs.option_a,
                        'option_b': mcqs.option_b,
                        'option_c': mcqs.option_c,
                        'option_d': mcqs.option_d,
                    }
                except Question_MCQS.DoesNotExist:
                    mcqs = None
                question_data['options'] = {} if mcqs is None else question_data['options']

            questions_with_options.append(question_data)

    if request.method == 'POST':
        score = 0
        
        for question in questions_with_options:
            answer_key = f'answer_{question["id"]}'
            if answer_key in request.POST:
                submitted_answer = request.POST[answer_key]
                correct_answer = None
                
                try:
                    if question['type'] == 'true_false':
                        correct_answer = Question_truefalse.objects.get(question_id=question['id']).answer
                    elif question['type'] == 'mcqs':
                        correct_answer = Question_MCQS.objects.get(question_id=question['id']).answer
                    elif question['type'] == 'fill_in_blank':
                        correct_answer = Question_fillblank.objects.get(question_id=question['id']).answer.lower()
                        submitted_answer = submitted_answer.lower()
                except Exception as e:
                    print(f"Error retrieving correct answer: {e}")
                
                is_correct = str(submitted_answer) == str(correct_answer)
                score += 10 if is_correct else 0
                
                # Create or update the Result object
                Result.objects.update_or_create(
                    student_id=student,
                    question_id=Question.objects.get(id=question["id"]),
                    lesson_id=lesson,
                    defaults={
                        'answer': submitted_answer,
                        'is_correct': is_correct,
                        'marks': 10 if is_correct else 0
                    }
                )
        
        return redirect('questions', lesson_id=lesson.id)

    questions_json = JsonResponse(questions_with_options, safe=False)
    
    context = {
        'questions': questions_with_options,
        'questions_json': questions_json.content.decode('utf-8'),
        'lesson': lesson,
    }
    
    return render(request, "student/quizing.html", context)
