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

#to do: use location from mask to determine max and min angles, then run openpose on them, or use a microphone to trigger a snapshot


#This is effectivly the main way to run this program. Currently two methods are written
#shoulderROM detects 6 range of motion parameters for the right or left shoulder
#runOP writes a batch file with a command to run openpose on a video, extracting anatomical locations
#runOP is general use, while shoulderROM is specific. Other jointROM functions will be added to obtain their ROM

#Index Relating index values to the 25 categories openpose generates
jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']
#shoulderROM
#dir : string for the path leading to ./framelook/rom/_romtype_ romtype is either lsrom, left shoulder ROM or rsrom, right shoulder ROM
#rom : is the ROM type i.e rsrom or lsrom
#isright a 1 or 0 value, if == 1 then joint is on anatomical right side. 
#Outputs : a json file in the dir folder listing all the motions and max/min values; 6 images to confirm the search algo and what it selected
def shoulderROM(dir,rom,isright):
    #paths to various folders
    rotpath = dir+rom+'rot'
    abpath = dir+rom+'abad'
    flexpath = dir+rom+'flex'
    vrotpath = dir+rom+'rotv.avi'
    vabpath = dir+rom+'abadv.avi'
    vflexpath = dir+rom+'flexv.avi'
    #selects the right shoulder or elbow and wrist. and if last value = 1 rotates cooridnate system by 180
    if isright == 1:
        flexlist = pOP.videoAngles(flexpath,2,4,0)
        rotlist = pOP.videoAngles(rotpath,3,4,0)
        ablist = pOP.videoAngles(abpath,2,4,1)
    #selects the left shoulder or elbow and wrist.
    else:
        flexlist = pOP.videoAngles(flexpath,5,7,1)
        rotlist = pOP.videoAngles(rotpath,6,7,1)
        ablist = pOP.videoAngles(abpath,5,7,0)
    #index of frame array, selects the max and min angle from horizontal 
    fmax,fmin = pOP.getMaxMinFrames(flexlist)
    rmax,rmin = pOP.getMaxMinFrames(rotlist)
    amax,amin = pOP.getMaxMinFrames(ablist)
    #adjust found angles to be in range normally reported for the specific measurment
    fv1 = flexlist[fmax]+90
    fv2 = flexlist[fmin]+90
    av1 = ablist[amax]+90
    av2 = ablist[amin]+90
    rv1 = rotlist[rmax]
    rv2 = rotlist[rmin]
    #formatting output
    fstr = 'Flexion is : '+str(fv1)+'| Extension is : '+str(fv2)
    rstr = 'Internal Rotation is : '+str(rv2)+'| External Rotation is : '+str(rv1)
    astr = 'Abduction is : '+str(av1)+'| Adduction is : '+str(av2)
    #output json
    djson = {
        "ROM Type":rom,
        "AbAd": {"Abduction": av1,"Adduction": av2},
        "Rot": {"Internal Rotation":rv2,"External Rotation":rv1},
        "Flex": {"Flexion":fv1,"Extension":fv2}            
            }
    #writes the output to the rom folder
    with open(str('./frameLook/rom/'+rom+'/'+rom+'data.json'),'w+') as f2:
        json.dump(djson,f2)
    #print to console
    print(rom)
    print(fstr)
    print(rstr)
    print(astr)
    #shows the found frames and writes found values to image title
    pOP.displayFrames(vrotpath,rmax,rmin,rotlist,'Rotation',0)
    pOP.displayFrames(vflexpath,fmax,fmin,flexlist,'Flexion',90)
    pOP.displayFrames(vabpath,amax,amin,ablist,'Abduction',90)
    cv.waitKey(0)

def shoulderROMFast(dir,rom,isright):
    #paths to various folders
    ipath=dir+rom
    rotpath = dir+rom+'rot'
    abpath = dir+rom+'abad'
    flexpath = dir+rom+'flex'
    vrotpath = dir+rom+'rotv.avi'
    vabpath = dir+rom+'abadv.avi'
    vflexpath = dir+rom+'flexv.avi'
    #selects the right shoulder or elbow and wrist. and if last value = 1 rotates cooridnate system by 180
    #name_arr = ['ab','ad','er','ir','fl','ex']
    if isright == 1:
        amax =pOP.imageAngles(0,ipath,2,4,1)
        amin =pOP.imageAngles(1,ipath,2,4,1)
        rmax =pOP.imageAngles(2,ipath,3,4,0)
        rmin =pOP.imageAngles(3,ipath,3,4,0)
        fmax = pOP.imageAngles(4,ipath,2,4,0)
        fmix = pOP.imageAngles(5,ipath,2,4,0)
    #selects the left shoulder or elbow and wrist.
    else:
        amax =pOP.imageAngles(0,ipath,5,7,0)
        amin =pOP.imageAngles(1,ipath,5,7,0)
        rmax =pOP.imageAngles(2,ipath,6,7,1)
        rmin =pOP.imageAngles(3,ipath,6,7,1)
        fmax = pOP.imageAngles(4,ipath,5,7,1)
        fmin = pOP.imageAngles(5,ipath,5,7,1)
    #index of frame array, selects the max and min angle from horizontal 
    
    #adjust found angles to be in range normally reported for the specific measurment
    fv1 = fmax+90
    fv2 = fmin+90
    av1 = amax+90
    av2 = amin+90
    rv1 = rmax
    rv2 = rmin
    #formatting output
    fstr = 'Flexion is : '+str(fv1)+'| Extension is : '+str(fv2)
    rstr = 'Internal Rotation is : '+str(rv2)+'| External Rotation is : '+str(rv1)
    astr = 'Abduction is : '+str(av1)+'| Adduction is : '+str(av2)
    #output json
    djson = {
        "ROM Type":rom,
        "AbAd": {"Abduction": av1,"Adduction": av2},
        "Rot": {"Internal Rotation":rv2,"External Rotation":rv1},
        "Flex": {"Flexion":fv1,"Extension":fv2}            
            }
    #writes the output to the rom folder
    with open(str('./frameLook/romI/'+rom+'data.json'),'w+') as f2:
        json.dump(djson,f2)
    #print to console
    print(rom)
    print(fstr)
    print(rstr)
    print(astr)
    #shows the found frames and writes found values to image title
    

    abi = cv.imread(dir+'ab_rendered.png')
    adi = cv.imread(dir+'ad_rendered.png')
    eri = cv.imread(dir+'er_rendered.png')
    iri = cv.imread(dir+'ir_rendered.png')
    fli = cv.imread(dir+'fl_rendered.png')
    exi = cv.imread(dir+'ex_rendered.png')
    shift=90
    cv.imshow('Abduction Max | Degrees:'+str(amax+shift),abi)
    cv.imshow('Abduction Min | Degrees:'+str(amin+shift),adi)
    cv.imshow('Rotation Max | Degrees:'+str(rmax),eri)
    cv.imshow('Rotation Min | Degrees:'+str(rmin),iri)
    cv.imshow('Flexion Max | Degrees:'+str(fmax+shift),fli)
    cv.imshow('Flexion Min | Degrees:'+str(fmin+shift),exi)

    cv.waitKey(0)

#runOP to be run on raw video and extract anatomical locations, and format into a more friendly format
#rom : name of the joint rom like lsrom or rsrom
#subrom : name of the sub motion, specific for each joint. for the shoulder 'flex', 'abad', and 'rot' represent the three motions that make up the joint rom
#Output : formatted data in the strucutre of rom/subrom[s] in each folder is 26 jsons with the X-Y position at each frame
def runOP(rom,subrom):
    #counter counts the number of frames in the video
    counter = 0
    vidtitle = rom+subrom
    #the command in the bat file, starts openposedemo.exe on --video which points to the video path, --net_resolution resolution of model, --write_json json output, --write_video video output
    batstr = 'START '+mglob.opathbin+' --video '+mglob.opath+'rawvid/'+rom+'/'+vidtitle+'.mp4 --net_resolution -1x256 --write_json '+mglob.outjson_path+' --write_video '+mglob.framelookpath+'rom/'+rom+'/'+vidtitle+'v.avi'
    
    #clean output folder
    for f in os.listdir(mglob.outjson_path):
        os.remove(os.path.join(mglob.outjson_path,f))
    #creates batfile in openpose path
    batfile = open(mglob.opath+'runop.bat','w')
    #magic words to change working directory
    sstr = "cd \"%~dp0\"\n"
    #writes the batfile
    batfile.write(sstr)
    batfile.write(batstr)
    batfile.close()
    #runs batfile
    sp.call(mglob.opath+'runop.bat')
    #due to design, the program will run all 3 bat files. this holds after each bat file. wait until each video is processed by openpose
    input("Wait until video is done please :")
    
    #counts the files in outputjson, each json is for 1 frame
    for f in os.listdir(mglob.outjson_path):
        counter = counter+1
        print(counter)
    #deprecated str
    procstr = mglob.opath+'processed/'+rom+'/'+vidtitle
    #from frame 0 to counter from mglob.outjson framelook output
    dget.processOverTime(0,counter,mglob.outjson_path,procstr,rom,subrom)

def runOPFast (rom):
#counter counts the number of frames in the video
    counter = 0
    #title = rom+subrom
    #the command in the bat file, starts openposedemo.exe on --video which points to the video path, --net_resolution resolution of model, --write_json json output, --write_video video output
    batstr = 'START '+mglob.opathbin+' --image_dir '+mglob.opath+'rawimg/'+rom+'/ --net_resolution -1x256 --write_json '+mglob.outjson_path+' --write_images '+mglob.framelookpath+'romI/'
    
    #clean output folder
    for f in os.listdir(mglob.outjson_path):
        os.remove(os.path.join(mglob.outjson_path,f))
    #creates batfile in openpose path
    batfile = open(mglob.opath+'runop.bat','w')
    #magic words to change working directory
    sstr = "cd \"%~dp0\"\n"
    #writes the batfile
    batfile.write(sstr)
    batfile.write(batstr)
    batfile.close()
    #runs batfile
    sp.call(mglob.opath+'runop.bat')
    #due to design, the program will run all 3 bat files. this holds after each bat file. wait until each video is processed by openpose
    input("Wait until video is done please :")
    
    #counts the files in outputjson, each json is for 1 frame
    for f in os.listdir(mglob.outjson_path):
        counter = counter+1
        print(counter)
    subrom='hold'
    #from frame 0 to counter from mglob.outjson framelook output
    dget.processOverTimeFast(0,counter,mglob.outjson_path,rom)

#runs OP for one motion type and for three different videos.lsrom + flex, rot and abad are video names to process

#runOP('lsrom','flex')
#runOP('lsrom','rot')
#runOP('lsrom','abad')
#runOPFast('lsrom')
#paths to each rom data sets
#jointcomplexpath = './framelook/rom/rsrom/'
#jointcomplexpath1 = './framelook/rom/lsrom/'
jointcomplexpath1 = './framelook/romI/'
#takes the reformated OP output, selects a path, joint rom and boolean flipper and autodetects extreme joint angles
shoulderROMFast(jointcomplexpath1,'lsrom',0)
#shoulderROM(jointcomplexpath1,'lsrom',0)