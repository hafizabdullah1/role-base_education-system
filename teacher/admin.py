from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Class)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Question_fillblank)
admin.site.register(Question_MCQS)
admin.site.register(Question_truefalse)
admin.site.register(Result)