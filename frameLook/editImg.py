import numpy as np
import cv2 as cv
import math

#to do the XY coordinates are wrong need to fix before doing polar crap the 
#file format is (y,x) 720 pixels tall increasing going down, 1280 pixels wide increasing going right
path = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\'
outpath = 'E:\\Users\\Michael\\OBSVid\\frameLook output\\out\\'
def simpLoadImg(path,framenum):
    filename = str("frame"+str(framenum)+".jpg")
    path1 = str(path+filename)
    return cv.imread(path1),filename


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
    #print("Origin is: "+str(origin))
    #print("UnShifted X: "+str(x)+" Y: "+str(y))
    if x>0 and y>0:
        x,y = int(x)+origin[0],int(y)+origin[1]
    elif x>0 and y<0:
        x,y = int(x)+origin[0],int(y)+origin[1]
    elif x<0 and y>0:
        x,y = int(x)+origin[0],int(y)+origin[1]
    elif x<0 and y<0:
        x,y = int(x)+origin[0],int(y)+origin[1]
    else:
        x,y = origin[0],int(y)+origin[1]
    #print("Shifted X: "+str(x)+" Y: "+str(y))
    
    return x,y
def findArc(angle,radius):
    arclength = angle*radius
    return arclength
def makeQuasiCircle(im,center,radius):
    cv.circle(im,center,int(radius-7),(255,255,255),thickness=-1)
    cv.circle(im,center,int(radius+22),(255,255,0),thickness=25)
def conArcArray(point1,point2,origin,samplecount):
    angle1 = findAngle(origin,point1)
    angle2 = findAngle(origin,point2)
    angledelta = angle1-angle2
    print("Angle1 :"+str(angle1)+" Angle2 :"+str(angle2)+" AngleDelta :"+str(angledelta))
    theta = np.linspace(angle1,angle2,num=samplecount)
    return theta
    
im,filename = simpLoadImg(path,79)
print(im.shape)
center = (490,540)
point = (917,246)
point1=(785,110)
point2=(1020,560)
im = putMarker(im,point2[0],point2[1])
findAngle(center,point2)
angle = findAngle(center,point)
r = findDist(center,point)
#makeQuasiCircle(im,center,r)
#im = putMarker(im,point2[0],point2[1])
im = putMarker(im,center[0],center[1])
arcmat = conArcArray(point1,point2,center,500)

def exportSeries(inpath,outpath,im,center,radius,startframe,endframe):
    for x in range(startframe,endframe):
        im,filename = simpLoadImg(inpath,x)
        print(im.shape)
        makeQuasiCircle(im,center,radius)
        im = putMarker(im,center[0],center[1])
        cv.imwrite(str(outpath+"out"+filename),im)

#exportSeries(path,outpath,im,center,r,50,100)
#thetaarr= conThetaVector(500,9)
rarr = []
garr = []
barr = []
colorarr =[]
#for z in arcmat:
 #   x,y = polarLoc(center,z,r)
  #  rarr,garr,barr = np.append(rarr,im[y,x][2]),np.append(garr,im[y,x][1]),np.append(barr,im[y,x][0])
#colorarr = (arcmat,rarr,garr,barr)
#print(colorarr)
#np.savetxt(outpath+'degreeRGBmatframe79.csv',colorarr,delimiter=',' ,fmt='%3f')
showIt(im)


