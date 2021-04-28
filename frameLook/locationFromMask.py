import cv2 as cv
import numpy as np
import myglobal as mglob
import editImg


b_x =[]
b_y =[]
clx =[]
cly =[]
baseim = cv.imread('./armc.png')
im1 = cv.imread('./outmasks/blue.jpg')
im2 = cv.imread('./outmasks/blue.jpg')
im3 = cv.imread('./outmasks/blue.jpg')
def getDim(img):
    height, width, channels = img.shape
    print("Height Is: "+str(height)+" Width is: "+str(width)+" Channels is: "+str(channels))
    return height,width,channels
def markerFindLength(mheight,mwidth):
    if mheight>mwidth:
        len1=int(mwidth/3)
    else:
        len1=int(mheight/3)
    if len1<350:
        len1=350
    return len1
def click_event(event,x,y,flags,params):
    global clx
    global cly
    if event == cv.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        clx.append(x)
        cly.append(y)
        return x,y
#finds the x y size of the marker using user input
cv.imshow('Select Range',baseim)
cv.setMouseCallback('Select Range',click_event)
cv.waitKey(0)
cv.destroyAllWindows()
h1 = abs(cly[0]-cly[1])
w1 = abs(clx[0]-clx[1])


h,w,c = getDim(mglob.bm)
#find relationship between the image size and what spacing is needed for N sample lines in the smallest dimension
N = 20
if h>w:
    det = int(w/N)
else:
    det = int(h/N)

#the third term in the for loop is the resolution, in this case 10 is 10x less points sampled
reso = det

finereso = int(reso/(reso/10))

length=markerFindLength(h1,w1)
shifttermh = h-(2+reso)
shifttermw = w-(2+reso)
for x in range(0,shifttermw,reso):
    for y in range(4,shifttermh,reso):        
        
        if mglob.bm[y][x][0] > 200:
            b_x.append(x)
            b_y.append(y)
            im1 = editImg.putMarker(im1,x,y)
#print(b_x)
#takes in a single blue gross match, and length/2 of search square centered on the point and finds how many red and green are in square
def matchSum(bluex,bluey,length,resolution):
    greencount =0
    redcount =0
    xmax,ymax,xmin,ymin = makeSearchArea(bluex,bluey,length)
    #print('Xmax: '+str(xmax)+' Xmin: '+str(xmin)+' YMax: '+str(ymax)+' YMin:'+str(ymin)) (2+resolution)
    for ax in range(xmin,xmax,resolution):
        for ay in range(ymin,ymax,resolution):
            if mglob.gm[ay][ax][0] > 200:
                greencount = greencount+1
            elif mglob.rm[ay][ax][0] > 200:
                redcount = redcount+1
    #print("Greens: "+str(greencount)+" Reds: "+str(redcount))
    return greencount,redcount
def makeSearchArea(bluex,bluey,length):
    xmax = bluex+length
    ymax = bluey+length
    xmin = bluex-length
    ymin = bluex-length
    
    if xmax >= mglob.width:
        xmax = mglob.width-1
    if ymax >= mglob.height:
        ymax = mglob.height-1
    if xmin < 0:
        xmin = 0
    if ymin < 0:
        ymin = 0
    return xmax,ymax,xmin,ymin

positiveblue_x = []
positiveblue_y = []

for x1 in range(0,len(b_x)):
    gc, rc = matchSum(b_x[x1],b_y[x1],length,finereso)
    threshold = 50
    if gc > threshold and rc > threshold:
        positiveblue_x.append(b_x[x1])
        positiveblue_y.append(b_y[x1])
        im2 = editImg.putMarker(im2,b_x[x1],b_y[x1])
def getMarkerLoc(pbx,pby):
    xloc = int(sum(pbx)/len(pbx))
    yloc = int(sum(pby)/len(pby))
    
    return xloc,yloc
xl,yl = getMarkerLoc(positiveblue_x,positiveblue_y)
print("The Marker Location is ("+str(xl)+', '+str(yl)+')')
im3 = editImg.putMarker(im3,xl,yl)
cv.imshow('blues',im1)
cv.imshow('blues post correct',im2)
cv.imshow('Location',im3)
cv.waitKey(0)





