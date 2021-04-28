import json
import numpy as np
path = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output_jsons"
path2 = r"C:/Users\Micheal\Desktop\Openposeattempts\openpose\output"

jointindx = ['0Nose','1Neck','2RShoulder','3RElbow','4RWrist','5LShoulder','6LElbow','7LWrist','8MidHip','9RHip','10RKnee','11RAnkle','12LHip','13LKnee','14LAnkle','15REye','16LEye','17REar','18LEar','19LBigToe','20LSmallToe','21LHeel','22RBigToe','23RSmallToe','24RHeel','25Background']

def dataOverTime(startF,endF,jointind,inpath,outpath):
    n = jointind
    xarr = []
    yarr = []
    jsonout = {}
    confidencearr = []
    for x in range(startF,endF):
        formatnum = str(x).zfill(12)
        #print(x)

        file = open(inpath+r"\romraise2_"+formatnum+r"_keypoints.json")
        data = json.load(file)
        xarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+0)])
        yarr.append(data['people'][0]['pose_keypoints_2d'][(n*3+1)])
        confidencearr.append(data['people'][0]['pose_keypoints_2d'][(n*3+2)])
    #print(xarr)
    jsonout['X']= xarr
    jsonout['Y']= yarr
    jsonout['Confidence'] =confidencearr

    with open(str(outpath+'\out'+jointindx[n]+'.json'),'w') as f:
        json.dump(jsonout,f)
def processOverTime(startF,endF,inpath,outpath):
    for z in range(0,25):
        dataOverTime(startF,endF,z,path,path2)
processOverTime(50,80,path,path2)