import plotly.express as px
import json
import opDataGet as dget
import plotOP as pOP
import numpy as np
import math
import cv2 as cv


path = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output"
jointcomplexpath = './shoulderrom/'


jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']
# isright = 1 if right, 0 if not
def shoulderROM(dir,isright):
    rotpath = dir+'rotation'
    abpath = dir+'abductionadduction'
    flexpath = dir+'flexionextension'
    vrotpath = dir+'video/rotation.avi'
    vabpath = dir+'video/abductionadduction.avi'
    vflexpath = dir+'video/flexionextension.avi'
    
    if isright == 1:
        flexlist = pOP.videoAngles(flexpath,2,4,0)
        rotlist = pOP.videoAngles(rotpath,3,4,0)
        ablist = pOP.videoAngles(abpath,2,4,1)
    else:
        flexlist = pOP.videoAngles(flexpath,5,7,1)
        rotlist = pOP.videoAngles(rotpath,6,7,1)
        ablist = pOP.videoAngles(abpath,5,7,0)

    fmax,fmin = pOP.getMaxMinFrames(flexlist)
    rmax,rmin = pOP.getMaxMinFrames(rotlist)
    amax,amin = pOP.getMaxMinFrames(ablist)
    fv1 = flexlist[fmax]+90
    fv2 = flexlist[fmin]+90
    av1 = ablist[amax]+90
    av2 = ablist[amin]+90
    rv1 = rotlist[rmax]
    rv2 = rotlist[rmin]
    fstr = 'Flexion is : '+str(fv1)+'| Extension is : '+str(fv2)
    rstr = 'Internal Rotation is : '+str(rv2)+'| External Rotation is : '+str(rv1)
    astr = 'Abduction is : '+str(av2)+'| Adduction is : '+str(av1)
    print(fstr)
    print(rstr)
    print(astr)
    pOP.displayFrames(vrotpath,rmax,rmin,rotlist,'Rotation')
    pOP.displayFrames(vflexpath,fmax,fmin,flexlist,'Flexion')
    pOP.displayFrames(vabpath,amax,amin,ablist,'Abduction')
    cv.waitKey(0)
shoulderROM(jointcomplexpath,1)