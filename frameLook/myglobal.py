import cv2 as cv
workingdir = "./framelook/outmasks/"
bm = cv.imread(workingdir+'blue.jpg')
gm = cv.imread(workingdir+'green.jpg')
rm = cv.imread(workingdir+'red.jpg')
clicklist = []
height, width, channels = bm.shape
