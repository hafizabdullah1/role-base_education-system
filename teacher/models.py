from django.db import models
from user_accounts.models import CustomUser

# # Create your models here.

class Cohort(models.Model):
    name                        = models.CharField(max_length=255, null=False)


class Class(models.Model):
    name                        = models.CharField(max_length=255)
    teacher_id                  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    name                        = models.CharField(max_length=255)
    teacher_id                  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_id                    = models.ForeignKey(Class, on_delete=models.CASCADE)

    
class Question(models.Model):
    type                        = models.CharField(max_length=50)
    statement                   = models.TextField(max_length=255)
    lesson_id                   = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    

class Question_truefalse(models.Model):
    question_id                 = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer                      = models.BooleanField(default=False)
    

class Question_MCQS(models.Model):
    question_id                 = models.ForeignKey(Question,on_delete=models.CASCADE)
    option_a                    = models.CharField(max_length=255)
    option_b                    = models.CharField(max_length=255)
    option_c                    = models.CharField(max_length=255)
    option_d                    = models.CharField(max_length=255)
    answer                      = models.CharField(max_length=255)
    
    
class Question_fillblank(models.Model):
    question_id                 = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer                      = models.CharField(max_length=255)
    

class Assign_Cohort(models.Model):
    user_id             = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cohort_id           = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    
    
class Result(models.Model):
    marks                   = models.IntegerField(default=0)
    lesson_id               = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user_id             = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_id             = models.ForeignKey(Question, on_delete=models.CASCADE)

