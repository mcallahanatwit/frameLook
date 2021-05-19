import plotly.express as px
import json
import opDataGet as dget
import plotOP as pOP
import numpy as np
import math
import cv2 as cv
import os
import subprocess as sp

opath = r'C:/Users/Micheal/Openpose/openpose/'
opathbin = r'C:/Users/Micheal/Openpose/openpose/bin/OpenPoseDemo.exe'

path = r"C:/Users/Micheal/openpose/openpose/output_jsons"
path2 = r"C:/Users/Micheal/openpose/openpose/output"
jointcomplexpath = './rom/rsrom/'


jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']
# isright = 1 if right, 0 if not
def shoulderROM(dir,isright):
    rotpath = dir+'rsromrot'
    abpath = dir+'rsromabad'
    flexpath = dir+'rsromflex'
    vrotpath = dir+'rsromrotv.avi'
    vabpath = dir+'rsromabadv.avi'
    vflexpath = dir+'rsromflexv.avi'
    
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
    pOP.displayFrames(vrotpath,rmax,rmin,rotlist,'Rotation',0)
    pOP.displayFrames(vflexpath,fmax,fmin,flexlist,'Flexion',90)
    pOP.displayFrames(vabpath,amax,amin,ablist,'Abduction',90)
    cv.waitKey(0)
def runOP(rom,subrom):
    counter = 0
    vidtitle = rom+subrom
    batstr = 'START C:/Users/Micheal/Openpose/openpose/bin/OpenPoseDemo.exe --video C:/Users/Micheal/Openpose/openpose/rawvid/'+rom+'/'+vidtitle+'.mp4 --net_resolution -1x256 --write_json C:/Users/Micheal/Openpose/openpose/output_jsons --write_video C:/Users/Micheal/source/repos/frameLook/frameLook/rom/'+rom+'/'+vidtitle+'v.avi'
    
    #clean output folder
    for f in os.listdir(path):
        #print(f)
        os.remove(os.path.join(path,f))
    
    batfile = open('C:/Users/Micheal/Openpose/openpose/runop.bat','w')
    sstr = "cd \"%~dp0\"\n"
    batfile.write(sstr)
    batfile.write(batstr)
    batfile.close()
    print('we here')
    #sp.run([opathbin,"--video=C:/Users/Micheal/Openpose/openpose/rawvids/"+rom+"/"+vidtitle+".mp4","--net_resolution= -1x256","--write_json=C:/Users/Micheal/Openpose/openpose/output_jsons", "--write_video=processed/"+rom+"/"+vidtitle+"v.avi"],cwd='C:/Users/Michael/Openpose/openpose')
    sp.call('C:/Users/Micheal/Openpose/openpose/runop.bat')
    input("Wait until video is done please :")
    
    print('we pass')
    for f in os.listdir(path):
        counter = counter+1
        print(counter)
    procstr = 'C:/Users/Micheal/Openpose/openpose/processed/'+rom+'/'+vidtitle
    dget.processOverTime(0,counter,path,procstr,rom,subrom)


runOP('rsrom','flex')
runOP('rsrom','rot')
runOP('rsrom','abad')
shoulderROM(jointcomplexpath,1)