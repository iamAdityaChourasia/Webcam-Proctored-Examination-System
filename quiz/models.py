from django.db import models

# Create your models here.

class Questions(models.Model):
    Qid = models.AutoField(primary_key=True)
    Ename = models.ForeignKey('Exams', on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)
    Question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=20)
    option2 = models.CharField(max_length=20)
    option3 = models.CharField(max_length=20)
    option4 = models.CharField(max_length=20)
    Answer = models.CharField(max_length=1)

class Exams(models.Model):
    Ename = models.CharField(max_length=50)
    Date = models.DateField()
    STime = models.TimeField()
    ETime = models.TimeField()
    QuestionCount = models.CharField(max_length=20)
    Tmarks = models.CharField(max_length=20)
    Duration = models.CharField(max_length=5)

class Marks(models.Model):
    Mid = models.AutoField(primary_key=True)
    Ename = models.ForeignKey('Exams', on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    marks = models.CharField(max_length=3)

class Warnings(models.Model):
    Wid = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Noface = models.IntegerField()
    Multiface = models.IntegerField()
    Ename = models.ForeignKey('Exams', on_delete=models.CASCADE)
