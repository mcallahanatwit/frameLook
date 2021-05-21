import plotly.express as px
import json
import opDataGet as dget
import plotOP as pOP
import numpy as np
import math
import cv2 as cv
import os
import subprocess as sp
import myglobal as mglob




jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']
# isright = 1 if right, 0 if not
def shoulderROM(dir,rom,isright):
    rotpath = dir+rom+'rot'
    abpath = dir+rom+'abad'
    flexpath = dir+rom+'flex'
    vrotpath = dir+rom+'rotv.avi'
    vabpath = dir+rom+'abadv.avi'
    vflexpath = dir+rom+'flexv.avi'
    
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
    astr = 'Abduction is : '+str(av1)+'| Adduction is : '+str(av2)
    djson = {
        "ROM Type":ROM,
        "AbAd": {"Abduction": av1,"Adduction": av2},
        "Rot": {"Internal Rotation":rv2,"External Rotation":rv1},
        "Flex": {"Flexion":fv1,"Extension":fv2}            
            }
    with open(str(outpath1+'/'+rom+'/'+sname+'/out'+jointindx[n]+'.json'),'w') as f2:
        json.dump(jsonout,f2)
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
    batstr = 'START '+mglob.opathbin+' --video '+mglob.opath+'rawvid/'+rom+'/'+vidtitle+'.mp4 --net_resolution -1x256 --write_json '+mglob.outjson_path+' --write_video '+mglob.framelookpath+'rom/'+rom+'/'+vidtitle+'v.avi'
    
    #clean output folder
    for f in os.listdir(mglob.outjson_path):
        #print(f)
        os.remove(os.path.join(mglob.outjson_path,f))
    
    batfile = open(mglob.opath+'runop.bat','w')
    sstr = "cd \"%~dp0\"\n"
    batfile.write(sstr)
    batfile.write(batstr)
    batfile.close()
    print('we here')
    sp.call(mglob.opath+'runop.bat')
    input("Wait until video is done please :")
    
    print('we pass')
    for f in os.listdir(mglob.outjson_path):
        counter = counter+1
        print(counter)
    procstr = mglob.opath+'processed/'+rom+'/'+vidtitle
    dget.processOverTime(0,counter,mglob.outjson_path,procstr,rom,subrom)


#runOP('lsrom','flex')
#runOP('lsrom','rot')
#runOP('lsrom','abad')
jointcomplexpath = './rom/lsrom/'
shoulderROM(jointcomplexpath,'lsrom',0)