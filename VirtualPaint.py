# Virtual Paint Project
##########################
import cv2
import  numpy as np
###########################

#setting the frame

frameWidth=1920
frameHeight=1080
cap=cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

###########################

myColors =  [0,70,154,76,255,255]#low,high hsv values to track the hsv values code is in the color picker code

myColorValues=[0,0,255] #bgr orange

myPoints =[]  #[x,y] the global points

def findColor(img,myColors,myColorValues):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints=[]
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHsv, lower, upper)
    x,y=getContours(mask)
    #
    cv2.circle(imgResult,(x,y),10,myColorValues,cv2.FILLED)  #its just a pointer to say where are we now
    if x!=0 and y!=0:
        newPoints.append([x,y])

    return newPoints


#get contour

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)

        if area>500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y


#to draw on every frame

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues,cv2.FILLED)



# running on every frame

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorValues)  #returns the new points for every frame
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("video",imgResult)

    k=cv2.waitKey(1)
    if k==ord('c'):                 #clears the screen if the button cq is pressed
        myPoints.clear()

    if k==27:                       #break if we press escape
        break

    if k==ord('s'):
        file_name=input("enter file name\n")   #takes the file name and save it
        cv2.imwrite(file_name+"scrnshot.jpg",imgResult)
        continue



cv2.destroyAllWindows()