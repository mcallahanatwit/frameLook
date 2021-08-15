import cv2 as cv
###########################################################
## EDIT THIS VARIBLE TO YOUR OPENPOSE FILE PATH          ##
opath = r'C:/Users/callahanm5/Openpose/openpose/'
## EDIT THIS VARIABLE TO YOUR FRAMELOOK FILE PATH        ##
framelookpath = 'C:/Users/callahanm5/source/repos/frameLookdemotest/frameLook/'
###########################################################
 
opathbin = opath+'bin/OpenPoseDemo.exe'
outjson_path = opath+'output_jsons'
opathoutput = opath+'output'
workingdir = "./framelook/outmasks/"

#framelookpath = 'C:/Users/Micheal/source/repos/frameLook/frameLook/'



clicklist = []

