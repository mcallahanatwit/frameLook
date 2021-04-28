import cv2 as cv
import math
import numpy as py

samplepath = './armcsample.png'
clx=[]
cly=[]
sample = cv.imread(samplepath)
height, width, channels = sample.shape 
print("Height Is: "+str(height)+" Width is: "+str(width)+" Channels is: "+str(channels))
print(sample[0][0])
def selectSampleRange(baseim):
   
    def click_event(event,x,y,flags,params):
        global clx
        global cly
        if event == cv.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
            clx.append(x)
            cly.append(y)
            return x,y
        #finds the x y size of the marker using user input
    cv.imshow('Select Leftmost Range',baseim)
    cv.setMouseCallback('Select Leftmost Range',click_event)
    cv.waitKey(0)
    cv.destroyAllWindows()
    pair1 = (clx[0],cly[0])
    pair2 = (clx[1],cly[1])
    print(pair1)
    return pair1,pair2
def formatPair(p1,p2):
    xdiff = p2[0]-p1[0]
    ydiff = p2[1]-p1[1]
    if xdiff<=0 or ydiff == 0:
        print("wrong entry select left first")
        exit(0)
    xrange=(p1[0],p2[0])
    if ydiff > 0:
        yrange = (p1[1],p2[1])
    else:
        yrange = (p2[1],p1[1])
    return xrange,yrange
def getSubImage(image,xrange,yrange):
    print((xrange[0],yrange[0]))
    print((xrange[1],yrange[1]))
    subim = image[yrange[0]:yrange[1],xrange[0]:xrange[1]]
    #print(subim)
    return subim
def getSampleImg(baseim):
    n1,n2 = selectSampleRange(baseim)
    xr,yr = formatPair(n1,n2)
    im = getSubImage(baseim,xr,yr)
    im = cv.resize(im,(500,500))
    return im

def readImg(path):
    img = cv.imread(path)
    return img
def getDim(img):
    height, width, channels = img.shape
    print("Height Is: "+str(height)+" Width is: "+str(width)+" Channels is: "+str(channels))
    return height,width,channels
def avgList(list):
    return sum(list)/len(list)
def avgBGR(img,shift):
    b=[]
    g=[]
    r=[]    
    h,w,c = getDim(img)
    for z in range(0,h):
        for y in range(0,w):
            b.append(img[z][y][0])
            g.append(img[z][y][1])
            r.append(img[z][y][2])
    b_avg = avgList(b)+shift
    g_avg = avgList(g)+shift
    r_avg = avgList(r)+shift
    return (int(b_avg),int(g_avg),int(r_avg))
def avgHSV(img,hs,ss,vs):
    hsv_img = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    h=[]
    s=[]
    v=[]    
    height,width,c = getDim(img)
    for z in range(0,height):
        for y in range(0,width):
            h.append(hsv_img[z][y][0])
            s.append(hsv_img[z][y][1])
            v.append(hsv_img[z][y][2])
    h_avg = avgList(h)+hs
    s_avg = avgList(s)+ss
    v_avg = avgList(v)+vs
    return (int(h_avg),int(s_avg),int(v_avg))
def makeAvgImg(img,bgr_mat):
    #print(bgr_mat[0][0])
    holderimg = img
    h,w,c=getDim(img)
    for z in range(0,h):
        for y in range(0,w):
            holderimg[z][y][0] = bgr_mat[0]
            holderimg[z][y][1] = bgr_mat[1]
            holderimg[z][y][2] = bgr_mat[2]
    holderimg = cv.resize(holderimg,(500,500))
    return holderimg
def showImgs(old,avg_result):
    #old = cv.resize(old,(500,500))
    cv.imshow("old", old)
    cv.imshow("avg_result",avg_result)
    cv.waitKey(0)
def colorGetter(path,hs,ss,vs):
    im1 = readImg(path)
    hsv = avgHSV(im1,hs,ss,vs)
    return hsv
def makeMaskLim(samplecolorimg):
    shift=15
    hsv = avgHSV(samplecolorimg,0,0,0)
    upperthresh = (hsv[0]+shift+90,255,255)
    lowerthresh = (hsv[0]-shift+90,50,50)
    print(upperthresh)
    print(lowerthresh)
largeimg = cv.imread('./armc.png')
daout = getSampleImg(largeimg)
cv.imshow('Out',daout)
cv.waitKey(0)
#imin = cv.imread(samplepath)
#hsv1 = colorGetter(samplepath,0,0,0)
#img1 = makeAvgImg(imin,hsv1)
#print(hsv1)
#makeMaskLim(img1)
#bgrimg1 = cv.cvtColor(img1, cv.COLOR_HSV2BGR)
#showImgs(sample,bgrimg1)

