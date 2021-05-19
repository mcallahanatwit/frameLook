import json
import numpy as np
path = r"C:/Users\Micheal\Openpose\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Openpose\openpose\output"

jointindx = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']

def dataOverTime(startF,endF,jointind,inpath,outpath,rom,subrom):
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
def processOverTime(startF,endF,inpath,outpath,rom,subrom):
    for z in range(0,25):
        dataOverTime(startF,endF,z,path,outpath,rom,subrom)
#processOverTime(0,260,path,path2)