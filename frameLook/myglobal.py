import cv2 as cv
workingdir = "./framelook/outmasks/"
#opath = r'C:/Users/Micheal/Openpose/openpose/'
opath = r'C:/Users/callahanm5/Openpose/openpose/'
opathbin = opath+'bin/OpenPoseDemo.exe'
outjson_path = opath+'output_jsons'
opathoutput = opath+'output'

framelookpath = 'C:/Users/Micheal/source/repos/frameLook/frameLook/'

#bm = cv.imread(workingdir+'blue.jpg')
#gm = cv.imread(workingdir+'green.jpg')
#rm = cv.imread(workingdir+'red.jpg')
clicklist = []
#height, width, channels = bm.shape
