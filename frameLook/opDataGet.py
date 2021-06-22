import json
import numpy as np
#path = r"C:/Users\Micheal\Openpose\openpose\output_jsons"
path = r"C:/Users\callahanm5\Openpose\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Openpose\openpose\output"

jointindx = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']

def dataOverTime(startF,endF,jointind,inpath,rom,subrom):
    outpath1 = 'C:/Users/Micheal/source/repos/frameLook/frameLook/rom'
    n = jointind
    sname = rom+subrom
    xarr = []
    yarr = []
    jsonout = {}
    confidencearr = []
    for x in range(startF,endF):
        formatnum = str(x).zfill(12)
        #print(x)
        strname = inpath+'/'+sname+'_'+formatnum+'_keypoints.json'
        
        file = open(strname)
        data = json.load(file)
        xarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+0)])
        yarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+1)])
        confidencearr.append(data['people'][0]['pose_keypoints_2d'][(n*3+2)])
    #print(xarr)
    jsonout['X']= xarr
    jsonout['Y']= yarr
    jsonout['Confidence'] =confidencearr
    
    
    with open(str(outpath1+'/'+rom+'/'+sname+'/out'+jointindx[n]+'.json'),'w') as f2:
        json.dump(jsonout,f2)

def dataOverTimeFast(startF,endF,jointind,inpath,rom):
    #outpath1 = 'C:/Users/Micheal/source/repos/frameLook/frameLook/romI'
    outpath1 = 'C:/Users/callahanm5/source/repos/frameLook/frameLook/romI'
    n = jointind
    sname = rom
    xarr = []
    yarr = []
    jsonout = {}
    confidencearr = []
    kp = '_keypoints.json'
    name_arr = ['ab'+kp,'ad'+kp,'er'+kp,'ir'+kp,'fl'+kp,'ex'+kp]
    for x in name_arr:
        #print(x)
        strname = inpath+'/'+x
        
        file = open(strname)
        data = json.load(file)
        xarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+0)])
        yarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+1)])
        confidencearr.append(data['people'][0]['pose_keypoints_2d'][(n*3+2)])
    #print(xarr)
    jsonout['X']= xarr
    jsonout['Y']= yarr
    jsonout['Confidence'] =confidencearr
    
    
    with open(str(outpath1+'/'+rom+'/out'+jointindx[n]+'.json'),'w') as f2:
        json.dump(jsonout,f2)    
def processOverTime(startF,endF,inpath,outpath,rom,subrom):
    for z in range(0,25):
        dataOverTime(startF,endF,z,path,outpath,rom,subrom)

def processOverTimeFast(startF,endF,inpath,rom):
    for z in range(0,25):
        dataOverTimeFast(startF,endF,z,path,rom)
#processOverTime(0,260,path,path2)