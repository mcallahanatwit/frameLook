import cv2 as cv
import numpy as np
import frameLook as fl

path = './vid/testpu.mp4'
outpath = './frameout/'

vid = fl.getCap(path)

def gFName(fnum):    
    gename = str('./frameout/frame'+str(fnum)+'.jpg')
    return gename

#Generates Frames to do analysis on

fl.makeFrames(vid,(50,60),outpath)

#Works on gen frames

img1 = cv.resize(cv.imread(gFName(50)),(200,150))
img3 = cv.resize(cv.imread(gFName(50)),(200,150))
img2 = cv.resize(cv.imread(gFName(51)),(200,150))

def f2fmove(img1,img2):
    nimg = img1
    c=0
    height, width, chanels = img1.shape
    print((height,width))
    thresh=150
    for h1 in range(0,height):
        for w1 in range(0,width):
            d1 = abs(img2[h1][w1][0]-img1[h1][w1][0])
            
            d2 = abs(img2[h1][w1][1]-img1[h1][w1][1])
            
            d3 = abs(img2[h1][w1][2]-img1[h1][w1][2])
            c=c+1
            if d1>=thresh or d2>=thresh or d3>=thresh:
                #d1=img2[h1][w1][0]
                #d2=img2[h1][w1][1]
                #d3=img2[h1][w1][2]
                d1=255
                d2=255
                d3=255
            else:
                d1=0
                d2=0
                d3=0
            difference = (d1,d2,d3)
            print(difference)
            nimg[h1][w1][0]= difference[0]
            nimg[h1][w1][1]= difference[1]
            nimg[h1][w1][2]= difference[2]
    print(c)
    return nimg
daimg=f2fmove(img1,img2)
cv.imshow('imgD',img3)
cv.imshow('img2',img2)
cv.imshow('d',daimg)
cv.waitKey(0)



