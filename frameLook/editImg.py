import numpy as np
import cv2 as cv
import math

#to do the XY coordinates are wrong need to fix before doing polar crap the 
#file format is (y,x) 720 pixels tall increasing going down, 1280 pixels wide increasing going right
path = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\frame100.jpg'
im = cv.imread(path)
print(im.shape)
def putMarker(img,x,y):
    xbounds = [x-5,x+5] 
    ybounds = [y-5,y+5]
    img[ybounds[0]:ybounds[1], xbounds[0]:xbounds[1]] = [255,255,0]
    return img
def showIt(im):
    cv.imshow("Video", im)
    cv.waitKey(0)
def findDist(pair1,pair2):
    xdelta = abs(pair1[0]-pair2[0])
    ydelta = abs(pair1[1]-pair2[1])
    dist = math.sqrt(xdelta*xdelta+ydelta*ydelta)
    print("The dist is: "+str(dist)+" Pixels")
    return dist
def findAngle(origin,pair1):
    
    offset = [-origin[0],-origin[1]]
    origin = np.add(origin,offset)
    relpair1 = np.add(pair1,offset)
    theta = math.atan(relpair1[1]/relpair1[0])
    print("Origin is: " +str(origin) + "| relative pair is "+str(relpair1)+"| Theta is " +str(theta))
    return theta
def polarLoc(origin,theta,radius):
    x = radius*math.cos(theta)
    y = radius*math.sin(theta)   
    if theta>0 :
        x,y = int(x)+origin[0],int(y)+origin[1]   
    elif theta<0 :
        x,y = -int(x)+origin[0],-int(y)+origin[1]
    else:
        x,y = origin[0],int(y)+origin[1]
    print("X: "+str(x)+" Y: "+str(y))
    return x,y
def findArc(angle,radius):
    arclength = angle*radius
    return arclength
def makeCircle(im,center,radius):
    cv.circle(im,center,int(radius),(0,255,255),thickness=2)

im = putMarker(im,597,113)
#im= putMarker(im,775,500)
#im = putMarker(im,380,482)
r = findDist([597,113],[380,482])
r1 = findDist([597,113],[775,500])
angle = findAngle([597,113],[380,482])
angle1 = findAngle([597,113],[775,500])
xtest1,ytest1 = polarLoc([597,113],angle1,r)
im = putMarker(im,xtest1,ytest1)
xtest,ytest = polarLoc([597,113],angle,r)
im = putMarker(im,xtest,ytest)
makeCircle(im,(597,113),r)
showIt(im)


