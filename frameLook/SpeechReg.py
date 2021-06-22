import speech_recognition as sr
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

def listen():
    # get audio from the microphone                                                                       
    r = sr.Recognizer()                                                                                   
    #while 1==1:
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)   
        speech = r.recognize_google(audio)
        print(speech)

    try:
        speech = r.recognize_google(audio)
        print("You said " + speech)
        if speech == "hello":
            print("we got it")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        #listen()
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
show_webcam()


    