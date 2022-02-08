from os import access
import cv2
import time
import random
from cv2 import VideoCapture
import numpy as np
start_time=time.time()
#starting the webcam
capture=cv2.VideoCapture(0)
#code ko sula rhe h jisse cam achee se open h jaye
time.sleep(2)
bg=0
fourcc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
#caputaring the background for 60 frames
for i in range(0,60):
    ret,bg=capture.read()
#flipping the bg
bg=np.flip(bg,axis=1)   
# read the caputre frame until camera is open
while(capture.isOpened()):
    ret,img=capture.read()
    if not ret:
        break
    img=np.flip(img,axis=1)

    #converting the color rgb to hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #generating mask to decet red color
    #these value can also be change as further color
    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,250])
    mask_1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask_2=cv2.inRange(hsv,lower_red,upper_red)

    mask_1= mask_1 +mask_2
    mask_1= cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1= cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask_2 = cv2.bitwise_not(mask_1) 
    #Keeping only the part of the images without the red color 
    #(or any other color you may choose) 
    res_1 = cv2.bitwise_and(img, img, mask=mask_2) 
    #Keeping only the part of the images with the red color 
    #(or any other color you may choose) 
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1) 
    #Generating the final output by merging res_1 and res_2 
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0) 
    output_file.write(final_output) 
    #Displaying the output to the user 
    cv2.imshow("magic", final_output) 
    cv2.waitKey(1)

capture.release() 
cv2.destroyAllWindows()


    






