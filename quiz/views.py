from django.shortcuts import render, redirect
from .models import *
import json
import datetime
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import threading
import queue
import cv2
import numpy as np
import time, os


ename=""
qcount=0
my_queue = queue.Queue()
camera_queue = queue.Queue()
# Create your views here.

def addExam(request):
    if request.user.is_authenticated:
        global ename
        global qcount
        Ename = request.POST['exam-name']
        QuestionCount = request.POST['question-count']
        TotalMarks = request.POST['total-marks']
        Duration = request.POST['duration']
        StartDate = request.POST['startdate']
        StartTime = request.POST['starttime'] + ":00"
        EndTime = request.POST['endtime'] + ":00"
        E = Exams(Ename=Ename,QuestionCount=QuestionCount,Tmarks=TotalMarks,Duration=Duration,Date=StartDate,STime=StartTime,ETime = EndTime)
        ename = E
        qcount = QuestionCount
        E.save()
        return render(request, 'AddQuestion.html')


def addQuestion(request):
    if request.user.is_authenticated:
        global qcount
        qcount = int(qcount)
        while(qcount):
            Marks = request.POST['marks']
            Question =  request.POST['question']
            Option1 = request.POST['optA']
            Option2 = request.POST['optB']
            Option3 = request.POST['optC']
            Option4 = request.POST['optD']
            Answer = request.POST['correct']
            Q = Questions(Ename=ename,marks=Marks,Question=Question,option1=Option1,option2=Option2,option3=Option3,option4=Option4,Answer=Answer)
            Q.save()
            qcount = qcount - 1
            return render(request, 'AddQuestion.html')
        return render(request, 'AddExam.html')

   
def showStudent(request):
    Mark = None
    if request.user.is_authenticated:
        E = Exams.objects.all()
        M = Marks.objects.all()
        for i in M:
            if i.Name == request.user.username:
                if i.Ename.Date == datetime.date.today():
                    if str(i.Ename.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.Ename.ETime) > datetime.datetime.now().strftime("%H:%M:%S"):
                        if i.marks:
                            Mark = True
                        else:
                            Mark = False
        Ex = dict()
        for i in E:
            if i.Date == datetime.date.today():
                if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S"):
                    Ex[i] = False
                else:
                    Ex[i] = True
        context = {'Exam':Ex, 'doneExam':Mark}
        return render(request, 'StudentPanel.html', context)

def startExam(request):
    def startEx(out_queue):
        if request.user.is_authenticated:
            questions = list()
            Q = Questions.objects.all()
            E = Exams.objects.all()
            t = None
            tmark = None
            stime=None
            etime=None
            for i in E:
                if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Date == datetime.date.today():
                    t = i.Duration
                    tmark = i.Tmarks
                    stime = i.STime 
                    etime = str(i.ETime)
                    eTime = etime
            ti = int(t)
            for i in Q:
                if str(i.Ename.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.Ename.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Ename.Date == datetime.date.today():
                    l = [i.Question,i.option1,i.option2,i.option3,i.option4,i.Answer,i.marks]
                    questions.append(l)
            question_list = json.dumps(questions)
            context = {'Time':ti, 'Question':question_list, 'Total':tmark}   
            out_queue.put(context)
            
    def startCamera():
        # importing_haarcascade_classifiers
        face_classifier =cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        # face_detection_function
        def face_detection(image):   
            # grascaling_image_passed
            if ret is True:
                gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  
                # detecting_faces    
                faces=face_classifier.detectMultiScale(gray,1.3,5)#1.6,7
                if len(faces)==0:
                    camera_queue.put("NO FACE DETECTED")   
                elif len(faces)>1:
                    camera_queue.put("MULTI FACE DETECTED") 
                else:
                    pass  
                # drawing_face_rectangle
                for (x,y,w,h) in faces:
                    # draw_rectangle_around_face     
                    cv2.rectangle(image,(x,y),(x+w,y+h),(127,0,255),2)           
            # returning_image_with_rectangles
            return image
        # capturing_video_from_webcam
        cap=cv2.VideoCapture(0)
        camera_queue.put(cap)
        while True:
            # reading_from_camera
            ret,frame=cap.read()
            face_detection(frame)
            # cv2.imshow('face_detection',face_detection(frame))
            time.sleep(5)
            # if_enter_pressed_then_exit
            if cv2.waitKey(1)==13:
                break        
        # releasing_camera
        cap.release()
        # destroying_window
        cv2.destroyAllWindows()

        print("HI CAMERA IS ON!!!")
    t1 = threading.Thread(target=startEx(my_queue))
    t1.start()
    t1.join()
    context = my_queue.get()
    t2 = threading.Thread(target=startCamera)
    t2.start()
    return render(request, 'ExamPanel.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'AddExam.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if request.user.username == 'minato':
                    return render(request, 'AddExam.html')
                else:
                    return redirect('/studentpanel')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return render(request,'Logout.html')

def Result(request):
    camera_queue.get().release()
        # destroying_window
    cv2.destroyAllWindows()

    nofaceCount = 0
    multifaceCount = 0

    while not camera_queue.empty():
        if camera_queue.get() == 'NO FACE DETECTED':
            nofaceCount += 1
        elif camera_queue.get() == 'MULTI FACE DETECTED':
            multifaceCount += 1
    print(nofaceCount, multifaceCount)
    username = request.user.username
    E = Exams.objects.all()
    en = None
    for i in E:
            if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Date == datetime.date.today():
                en = i
    res = request.POST['result']
    if not res:
        res = 0
    R = Marks(Name=username,Ename=en,marks=res)
    R.save()
    W = Warnings(Name=username,Noface=nofaceCount,Multiface=multifaceCount,Ename=en)
    W.save()
    return redirect('/studentpanel')
    
    