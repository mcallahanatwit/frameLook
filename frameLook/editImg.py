import numpy as np
import cv2 as cv
import math
from PIL import Image
#to do the XY coordinates are wrong need to fix before doing polar crap the 
#file format is (y,x) 720 pixels tall increasing going down, 1280 pixels wide increasing going right
path = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\frame50.jpg'
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
    x,y = -int(x)+origin[0],-int(y)+origin[1]    
    return x,y

#im = putMarker(im,597,113)
#im= putMarker(im,113,597)
#im = putMarker(im,380,482)
r = findDist([597,113],[380,482])
angle = findAngle([597,113],[380,482])
xtest,ytest = polarLoc([597,113],angle,r)
im = putMarker(im,xtest,ytest)
showIt(im)


