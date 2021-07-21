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
import editImg as eim

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
    ipath=dir+rom+'/'
    rotpath = dir+rom+'rot'
    abpath = dir+rom+'abad'
    flexpath = dir+rom+'flex'
    vrotpath = dir+rom+'rotv.avi'
    vabpath = dir+rom+'abadv.avi'
    vflexpath = dir+rom+'flexv.avi'
    #selects the right shoulder or elbow and wrist. and if last value = 1 rotates cooridnate system by 180
    #name_arr = ['ab','ad','er','ir','fl','ex']
    if isright == 1:
        amax, pairs1 =pOP.imageAngles(0,ipath,2,4,1)
        amin, pairs2 =pOP.imageAngles(1,ipath,2,4,1)
        rmax, pairs3 =pOP.imageAngles(2,ipath,3,4,0)
        rmin,pairs4 =pOP.imageAngles(3,ipath,3,4,0)
        fmax,pairs5 = pOP.imageAngles(4,ipath,2,4,0)
        fmin,pairs6 = pOP.imageAngles(5,ipath,2,4,0)
    #selects the left shoulder or elbow and wrist.
    else:
        amax, pairs1 =pOP.imageAngles(0,ipath,5,7,0)
        amin, pairs2 =pOP.imageAngles(1,ipath,5,7,0)
        rmax, pairs3 =pOP.imageAngles(2,ipath,6,7,1)
        rmin, pairs4 =pOP.imageAngles(3,ipath,6,7,1)
        fmax, pairs5 = pOP.imageAngles(4,ipath,5,7,1)
        fmin, pairs6 = pOP.imageAngles(5,ipath,5,7,1)
    #index of frame array, selects the max and min angle from horizontal 
    abi = cv.imread(ipath+'ab_rendered.png') 
    adi = cv.imread(ipath+'ad_rendered.png')
    eri = cv.imread(ipath+'er_rendered.png')
    iri = cv.imread(ipath+'ir_rendered.png')
    fli = cv.imread(ipath+'fl_rendered.png')
    exi = cv.imread(ipath+'ex_rendered.png')
    
    abi=eim.drawArc(abi,pairs1[0],pairs1[1],amax*math.pi/180-math.pi/2,.5*math.pi)
    adi=eim.drawArc(adi,pairs2[0],pairs2[1],amin*math.pi/180+math.pi*3/4,.5*math.pi)
    eri=eim.drawArc(eri,pairs3[0],pairs3[1],rmax*math.pi/180-math.pi/2,-math.pi)
    iri=eim.drawArc(iri,pairs4[0],pairs4[1],rmin*math.pi/180+math.pi/2,math.pi)
    fli=eim.drawArc(fli,pairs5[0],pairs5[1],fmax*math.pi/180-math.pi/2,.5*math.pi)
    exi=eim.drawArc(exi,pairs6[0],pairs6[1],fmin*math.pi/180+math.pi/8,.5*math.pi)
    
    #convert to degree
    
    fv1 = fmax*180/math.pi +90  
    fv2 = fmin*180/math.pi +90  
    av1 = amax*180/math.pi +90  
    av2 = amin*180/math.pi +90  
    rv1 = rmax*180/math.pi   
    rv2 = rmin*180/math.pi   
        
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
    dir = dir+rom+'/'

    
    
    
    cv.imshow('Abduction Max | Degrees:'+str(av1),abi)
    cv.imshow('Abduction Min | Degrees:'+str(av2),adi)
    cv.imshow('Rotation Max | Degrees:'+str(rv1),eri)
    cv.imshow('Rotation Min | Degrees:'+str(rv2),iri)
    cv.imshow('Flexion Max | Degrees:'+str(fv1),fli)
    cv.imshow('Flexion Min | Degrees:'+str(fv2),exi)

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
    batstr = 'START '+mglob.opathbin+' --image_dir '+mglob.opath+'rawimg/'+rom+'/ --net_resolution -1x256 --write_json '+mglob.outjson_path+' --write_images '+mglob.framelookpath+'romI/'+rom+'/'
    
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
def lookThruVid(vidpath,outputpath,iswebcam):
    x=1
    framenum=1
    print("Enter s to save frame, q to quit")
    if iswebcam==True:
        # define a video capture object
        vid = cv.VideoCapture(0)  
        while(True):      
            # Capture the video frame
            # by frame
            ret, frame = vid.read()
  
            # Display the resulting frame
            cv.imshow('Webcam', frame)
      
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            
            if cv.waitKey(1) == ord('s'):
                name = str(input('Enter name to save as: '))
                string1 = str(outputpath)+str(name)+'.png'
                cv.imwrite(string1,frame)
                print(string1)
            if cv.waitKey(1) == ord('q'):
                break
  
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv.destroyAllWindows()
    else:
        while x==1:
            img = pOP.findFrame(vidpath,framenum)
        
            cv.imshow('Frame is: '+str(framenum),img)
            key = chr(cv.waitKey(0))
            cv.destroyAllWindows()
            if key == 'q':
                print('End')
                x=2
            if key == '1':
                print('Advance 1 Frame')
                framenum=framenum+1
            if key == '2':
                print('Advance 5 Frames')
                framenum=framenum+5
            if key == '3':
                print('Advance 25 Frames')
                framenum=framenum+25
            if key == '4':
                print('Advance 50 Frames')
                framenum=framenum+50
            if key == '5':
                print('Back 1 Frame')
                framenum=framenum-1
            if key == '6':
                print('Back 5 Frames')
                framenum=framenum-5
            if key == '7':
                print('Back 25 Frames')
                framenum=framenum-25
            if key == '8':
                print('Back 50 Frames')
                framenum=framenum-50
            if key == 's':
                name = str(input('Enter name to save as: '))
                string1 = str(outputpath)+str(name)+'.png'
                cv.imwrite(string1,img)
                print(string1)




#runs OP for one motion type and for three different videos.lsrom + flex, rot and abad are video names to process
jointcomplexpath1 = './framelook/romI/'
routput = 'C:/Users/callahanm5/Openpose/openpose/rawimg/test1/'
vidpath = './framelook/vid/'
file = vidpath+'test.mp4'

#runOP('lsrom','flex')
#runOP('lsrom','rot')
#runOP('lsrom','abad')
#lookThruVid(file,routput,True)
#runOPFast('test')
#paths to each rom data sets
#jointcomplexpath = './framelook/rom/rsrom/'
#jointcomplexpath1 = './framelook/romI/'


#print(file)

#imt = pOP.findFrame(file,50)
#print(imt)
#cv.imshow('test',imt)
#key=cv.waitKey(0)
#print(chr(key))

#takes the reformated OP output, selects a path, joint rom and boolean flipper and autodetects extreme joint angles
#isright = int(input("1 for Right| 0 for left"))
isright=0
shoulderROMFast(jointcomplexpath1,'test',isright)
#shoulderROM(jointcomplexpath1,'lsrom',0)