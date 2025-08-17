import cv2
import numpy as np
import time

# importing_haarcascade_classifiers
face_classifier =cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
nofaceCount = 0
multifaceCount = 0

# face_detection_function
def face_detection(image):
    
    # grascaling_image_passed
    if ret is True:
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  
        
        # detecting_faces    
        faces=face_classifier.detectMultiScale(gray,1.3,5)#1.6,7
        
        if len(faces)==0:
            nofaceCount += 1
        elif len(faces)>1:
            multifaceCount += 1
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

while True:

    # reading_from_camera
    ret,frame=cap.read()
    cv2.imshow('face_detection',face_detection(frame))
    time.sleep(5)
    
    # if_enter_pressed_then_exit
    if cv2.waitKey(1)==13:
        break
        
# releasing_camera
cap.release()
# destroying_window
cv2.destroyAllWindows()
