import numpy as np
import cv2 as cv

path = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\'
outpath = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\out\\'
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
    
#vid =getCap("E:\\Users\\Michael\\OBSVid\\lwks output\\full arm swing.mp4")

def getFrame(cap,framenum,name,outpath):
    print(cap.get(cv.CAP_PROP_FRAME_COUNT))
    cap.set(cv.CAP_PROP_POS_FRAMES,framenum)
    ret, img = cap.read()
    cv.imwrite(outpath+"frame"+str(name)+".jpg",img)
    #cv.imshow("Video", img)
    #cv.waitKey(0)
def makeFrames(cap,framearray,outpath):
    for x in framearray:
        getFrame(cap,x,x,outpath)
def makeVid(startFrameNum,endFrameNum,path):
    out = cv.VideoWriter(str(outpath+'Output_video.avi'),cv.VideoWriter_fourcc(*'DIVX'),30,(1280,720))
    for x in range(startFrameNum,endFrameNum):
        img = cv.imread(path+'outframe'+str(x)+'.jpg')
        out.write(img)
    out.release()
#makeVid(50,100,outpath)
#for x in range(50,100):
 #   getFrame(vid,x,x,path)
