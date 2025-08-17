from django.contrib import admin
from quiz.models import *
# Register your models here.
admin.site.register(Questions)
admin.site.register(Exams)
admin.site.register(Marks)
admin.site.register(Warnings)