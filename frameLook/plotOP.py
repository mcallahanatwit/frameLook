import plotly.express as px
import json
import opDataGet as dget
import numpy as np
import math

path = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output"
apath = r'./framelook/shoulderrom/rotation'

jointchart = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']

def getFile(jointindx,path):
    name = str(path+'/out'+jointchart[jointindx]+'.json')
    file = open(name)
    data = json.load(file)
    x,y,c = data['X'],data['Y'],data['Confidence']
    file.close()
    return x,y,c
def plotJoint(joints,path):
    xall,yall,call = [],[],[]
    for x in joints:
        #print(x)
        x,y,c = getFile(x,path)
        xall.append(x),yall.append(y),call.append(c)
    #print(xall)
    
    fig = px.scatter(x=xall[0],y=yall[0])
    for z in range(1,len(joints)):
        
        #fig.add_scatter(x=xall[z],y=yall[z],mode="markers")
        fig.add_scatter(x=xall[z],y=yall[z],mode="markers")

    #print('we here')
    fig['layout']['yaxis']['autorange'] = "reversed"
    fig.update_yaxes(scaleanchor = "x",scaleratio = 1, )
    fig.show()

def plotJointRotated(joints,path,theta):
    xall,yall,call = [],[],[]
    for x in joints:
        #print(x)
        x,y,c = getFile(x,path)
        xrot,yrot =rotCoord((x,y),theta)
        xall.append(xrot),yall.append(yrot),call.append(c)
    #print(xall)
    fig = px.scatter(x=xall[0],y=yall[0])
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

def findAngle(origin,pair1,strname):
    
    offset = [-origin[0],-origin[1]]
    origin = np.add(origin,offset)
    relpair1 = np.add(pair1,offset)
    theta = (-math.atan(relpair1[1]/relpair1[0])+1*math.pi)*180/math.pi
    print('For'+str(strname)+' Origin is: ' +str(origin) + "| relative pair is "+str(relpair1)+"| Degree Theta is " +str(int(theta)))
    return theta
def rotCoord(pairlist,theta):
    dpair = pairlist
    print(len(pairlist[0]))
    for zz in range (0,len(pairlist[0])):
        dpair[0][zz] = int(pairlist[0][zz]*math.cos(-theta)-pairlist[1][zz]*math.sin(-theta))
        dpair[1][zz] = int(pairlist[0][zz]*math.sin(-theta)+pairlist[1][zz]*math.cos(-theta))
    return dpair[0],dpair[1]
desire = [3,4,2]
desireW = 4
desireS = 2
startframe =50
endframe = 200
lookframe = 50
modlookframe = lookframe-startframe
#dget.processOverTime(startframe,endframe,path,path2)
#cO=getCoords(desireS,modlookframe,startframe,path2)
#c2=getCoords(desireW,modlookframe,startframe,path2)
#findAngle(cO,c2)
plotJoint(desire,apath)
#using vlaues extracted from graph
rc = (504,-347)
ri = (581,-441)
re = (490,-221)
fc = (476,-339)
ff = (484,-60)
fe = (310,-519)
ac = (527,-341)
ab = (539,-95)
ad = (676,-510)
findAngle(rc,ri,'Rot Internal')
findAngle(rc,re,'Rot External')
findAngle(fc,ff,'Flexion')
findAngle(fc,fe,'Extension')
findAngle(ac,ab,'Abduction')
findAngle(ac,ad,'Adduction')
#plotJointRotated(desire,apath,.78)
