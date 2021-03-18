import numpy as np
import cv2 as cv

#loads video
def getCap(path):
    cap = cv.VideoCapture(path)
    return cap
def loadVid(cap):
    
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    
vid =getCap("E:\\Users\\Michael\\OBSVid\\lwks output\\swing test.mp4")

def getFrame(cap,framenum,name):
    print(cap.get(cv.CAP_PROP_FRAME_COUNT))
    cap.set(cv.CAP_PROP_POS_FRAMES,framenum)
    ret, img = cap.read()
    cv.imwrite("E:\\Users\\Michael\\OBSVid\\frameLook output\\frame"+str(name)+".jpg",img)
    #cv.imshow("Video", img)
    #cv.waitKey(0)

getFrame(vid,50,50)