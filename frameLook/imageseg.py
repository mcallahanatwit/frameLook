import cv2 as cv
import math
import numpy as py
import getColor
#taken from https://github.com/realpython/materials/tree/master/opencv-color-spaces
#
#This file creates three masks, from three color filters of red green and blue and saves them to ./outmasks/...
#
full = cv.imread('./armc.png')
#full = cv.imread('./wholecolors.png')

smallpath = './blue.png'
#cv.namedWindow('full',cv.WINDOW_KEEPRATIO)
#cv.imshow('full',full)
#cv.resizeWindow('full',76,173)
#cv.waitKey(0)
upper_blue = (40,255,255)
lower_blue = (0,75,75)
#upper_blue,lower_blue = getColor.getMaskFromSubImg(full)
print((upper_blue,lower_blue))
upper_green = (80,255,255)
lower_green = (40,75,75)
upper_red = (180,255,255)
lower_red = (90,100,75)

def maskImage(image,lowerbgr,upperbgr):

    hsv_full = cv.cvtColor(image,cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv_full,lowerbgr,upperbgr)
    result = cv.bitwise_and(image,image,mask=mask)
    return result, mask
def maskSave(image,lowerbgr,upperbgr,filename):
    hsv_full = cv.cvtColor(image,cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv_full,lowerbgr,upperbgr)
    cv.imwrite("./outmasks/"+filename+".jpg",mask)
    return mask
def makeBGRMask(image):    
    b_mask = maskSave(full,lower_blue,upper_blue,'blue')
    g_mask = maskSave(full,lower_green,upper_green,'green')
    r_mask = maskSave(full,lower_red,upper_red,'red')
    return b_mask,g_mask,r_mask
#cv.namedWindow('result',cv.WINDOW_KEEPRATIO)
b,g,r=makeBGRMask(full)
cv.imshow('blue_result',b)
#cv.imshow('green_result',g)
#cv.imshow('red_result',r)
finalout = cv.add(b,g)
finalout = cv.add(finalout,r)
cv.imshow('FinalOut',finalout)
#cv.resizeWindow('result',76,173)
cv.waitKey(0)