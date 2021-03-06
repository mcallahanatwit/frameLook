import plotly.express as px
import json
import opDataGet as dget
import numpy as np
import math
import cv2 as cv

path = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output"
rotpath = r'./shoulderrom/rotation'
abpath = r'./rom/rsrom/rsromabad'
flexpath = r'./shoulderrom/flexionextension'
vrotpath = r'./shoulderrom/video/rotation.avi'
vabpath = r'./shoulderrom/video/abductionadduction.avi'
vflexpath = r'./shoulderrom/video/flexionextension.avi'

jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']

def getFile(jointindx,path):
    name = str(path+'/out'+jointchart[jointindx]+'.json')
    file = open(name)
    data = json.load(file)
    x,y,c = data['X'],data['Y'],data['Confidence']
    file.close()
    return x,y,c
def plotJoint(joints,path,title):
    xall,yall,call = [],[],[]
    for x in joints:
        #print(x)
        x,y,c = getFile(x,path)
        xall.append(x),yall.append(y),call.append(c)
    #print(xall)
    
    fig = px.scatter(x=xall[0],y=yall[0],title=title)
    for z in range(1,len(joints)):
        
        #fig.add_scatter(x=xall[z],y=yall[z],mode="markers")
        fig.add_scatter(x=xall[z],y=yall[z],mode="markers")

    #print('we here')
    fig['layout']['yaxis']['autorange'] = "reversed"
    fig.update_yaxes(scaleanchor = "x",scaleratio = 1, )
    fig.show()

def plotJointRotated(joints,path,theta,title):
    xall,yall,call = [],[],[]
    for x in joints:
        #print(x)
        x,y,c = getFile(x,path)
        xrot,yrot =rotCoord((x,y),theta)
        xall.append(xrot),yall.append(yrot),call.append(c)
    #print(xall)
    fig = px.scatter(x=xall[0],y=yall[0],title=title)
    for z in range(1,len(joints)):
        #fig.add_scatter(x=xall[z],y=yall[z],mode="markers")
        fig.add_scatter(x=xall[z],y=yall[z],mode="markers")

    #print('we here')
    fig['layout']['yaxis']['autorange'] = "reversed"
    fig.update_yaxes(scaleanchor = "x",scaleratio = 1, )
    fig.show()
    
def getCoords(joint,framenum,startframe,path):   
    xall,yall,call = [],[],[]
    #print(joint)
    #print(framenum)
    x,y,c = getFile(joint,path)
    xall.append(x),yall.append(y),call.append(c)
    #print(xall)
    x,y = xall[0][framenum],yall[0][framenum]
    print('Joint: '+jointchart[joint]+'| Frame is: '+str(framenum+startframe)+'| X is: '+str(x)+'| Y is: '+str(y))
    
    return (x,y)

def getDist(p1,p2):
    xdiff = p1[0]-p2[0]
    ydiff = p1[1]-p2[1]
    return math.sqrt(xdiff*xdiff+ydiff*ydiff)

def findAngle(origin,pair1,strname,flipperbool):
    print('The Angle pairs are: '+str(origin)+' and '+str(pair1))
    offset = [-origin[0],-origin[1]]
    origin = np.add(origin,offset)
    relpair1 = np.add(pair1,offset)
    if flipperbool == False :
        print("we here")
        theta = (-math.atan2(relpair1[1],-relpair1[0]))
        
    if flipperbool == True:
        theta = (math.atan2(-relpair1[1],relpair1[0]))
        print('wack')
    print('For'+str(strname)+' Origin is: ' +str(origin) + "| relative pair is "+str(relpair1)+"| Degree Theta is " +str(int(theta)))
    return theta
def rotCoord(pairlist,theta):
    dpair = pairlist
    print(len(pairlist[0]))
    for zz in range (0,len(pairlist[0])):
        dpair[0][zz] = int(pairlist[0][zz]*math.cos(-theta)-pairlist[1][zz]*math.sin(-theta))
        dpair[1][zz] = int(pairlist[0][zz]*math.sin(-theta)+pairlist[1][zz]*math.cos(-theta))
    return dpair[0],dpair[1]
 
def videoAngles(jpath,DESIRE_origin_joint,DESIRE_far_joint,flipperbool):
    xo,yo,co = getFile(DESIRE_origin_joint,jpath)
    xf,yf,cf = getFile(DESIRE_far_joint,jpath)
    l1 = [] 
    cl= []
    for i in range(0,len(xo)):
        if cf[i]<= 0.5:
            xf[i]=xf[i-1]
            yf[i]=yf[i-1]
        name = 'Frame:'+str(i+1)
        angle = findAngle((xo[i],yo[i]),(xf[i],yf[i]),name,flipperbool)
        l1.append(angle)    
    return l1

def imageAngles(i,jpath,DESIRE_origin_joint,DESIRE_far_joint,flipperbool):
    xo,yo,co = getFile(DESIRE_origin_joint,jpath)
    xf,yf,cf = getFile(DESIRE_far_joint,jpath)
    FandOpairs = ((xf[i],yf[i]),(xo[i],yo[i]))
    name_arr = ['ab','ad','er','ir','fl','ex']
    angle = findAngle((xo[i],yo[i]),(xf[i],yf[i]),name_arr[i],flipperbool)
    print('Angle is: '+str(angle*180/math.pi))
    return angle, FandOpairs
def demoAngles(jpath,origin_joint,far_joint,direction):
    xo,yo,co = getFile(origin_joint,jpath)
    xf,yf,cf = getFile(far_joint,jpath)
    i=0
    name_arr = ['demo']    
    flipperbool=True
    if origin_joint in [5,6,7,12,13,14,19,20,21]:
        print('test1')
        flbool=False
    else:
        print('test2')
        flipperbool= True
    
    if direction=='u':
        shiftx=0
        shifty=100
        
    elif direction=='d':
        shiftx=0
        shifty=-100
        
    elif direction=='l':
        shiftx=100
        shifty=0 
        
    elif direction=='r':        
        shiftx=-100
        shifty=0
        
    angle = findAngle((xo[i],yo[i]),(xf[i],yf[i]),name_arr[i],True)
       
    
    groundlinepair = (xo[i]+shiftx,yo[i]-shifty)
    angle1 = findAngle((xo[i],yo[i]),groundlinepair,name_arr[i],flipperbool)
    pair_o = (int(xo[i]),int(yo[i])) ; pair_f = (int(xf[i]),int(yf[i])); groundlinepair = (int(xo[i]+shiftx),int(yo[i]-shifty))
    return angle-angle1, pair_o, pair_f, groundlinepair
def findGroundLinePoint(origin,distance,radian):
    xnew = int(distance*math.cos(radian)+origin[0])
    ynew = int(distance*math.sin(radian)+origin[1])
    print((xnew,ynew))
    #return(int(origin[0]),int(origin[1]))
    return (xnew,ynew)

def getMaxMinFrames(aglist):
    max_value = max(aglist)
    min_value = min(aglist)
    max_i = aglist.index(max_value)
    min_i = aglist.index(min_value)
    #print("Min Angle Frame: "+str(min_i+1)+' Degrees: '+str(min_value)+ ' | MAx Angle Frame:'+str(max_i+1)+' Degrees: '+str(max_value))
    return max_i,min_i
def displayFrames(videopath,max_i,min_i,aglist,name,shift):
    
    cap = cv.VideoCapture(videopath)
    cap.set(cv.CAP_PROP_POS_FRAMES,max_i)
    ret1, maxframe = cap.read()
    cap.set(cv.CAP_PROP_POS_FRAMES,min_i)
    ret2, minframe = cap.read()
    cv.imshow(str(name)+' Max | Degrees:'+str(aglist[max_i]+shift),maxframe)
    cv.imshow(str(name)+' Min | Degrees:'+str(aglist[min_i]+shift),minframe)
    
def findFrame(videopath,framenum):
    cap = cv.VideoCapture(videopath)
    cap.set(cv.CAP_PROP_POS_FRAMES,framenum)
    ret1, frame = cap.read()
    return frame
#desire = [3,4,2]
#desireW = 4
#desireS = 2
#startframe =50
#endframe = 200
#lookframe = 50
#modlookframe = lookframe-startframe
#dget.processOverTime(startframe,endframe,path,path2)
#cO=getCoords(desireS,modlookframe,startframe,path2)
#c2=getCoords(desireW,modlookframe,startframe,path2)
#findAngle(cO,c2)
#flexlist = videoAngles(flexpath,2,4,0)
#rotlist = videoAngles(rotpath,3,4,0)
#ablist = videoAngles(abpath,2,4,1)
#fmax,fmin = getMaxMinFrames(flexlist)
#rmax,rmin = getMaxMinFrames(rotlist)
#amax,amin = getMaxMinFrames(ablist)
#displayFrames(vrotpath,rmax,rmin,rotlist,'Rotation')
#displayFrames(vflexpath,fmax,fmin,flexlist,'Flexion')
#displayFrames(vabpath,amax,amin,ablist,'Abduction')
#cv.waitKey(0)
#plotJoint(desire,abpath,'Ab Ad')
#plotJoint(desire,flexpath,'Fl Ex')
#plotJoint([3,4],rotpath,'Rot')
#using vlaues extracted from graph

