import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

HEIGHT=3264

# Function to predict the distance based on the resolution
def predictDistance(img):
   try:
      if img == None:
         return
   except:
      expected = np.array([2290,2770,2110,2550,1710,2065,1230, \
                           1490,760,915,325,390])
      h,w,c=img.shape
      current = np.array([w,h,w,h,w,h,w,h,w,h,w,h])
      res=np.subtract(expected,current)
      A=([1,1,0,0,0,0,0,0,0,0,0,0],
         [0,0,1,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,1,1,0,0,0,0,0,0],
         [0,0,0,0,0,0,1,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,1,1,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,1])
      res=np.matmul(A,res)
      return np.argmin(np.power(res,2))

imgs = [f for f in listdir('dst/') if isfile(join('dst/', f))]

distances=['Close(Front)','Medium(Front)','Far(Front)','Close(Back)', \
           'Medium(Back)','Far(Back)']

counter=1
for i in range(0,len(imgs),2):
   if i+1 < len(imgs):
      img1=cv2.imread('dst/'+imgs[i])
      t=distances[predictDistance(img1)]
      factor = HEIGHT/img1.shape[0]
      img1 = cv2.resize(img1,(0,0),fx=factor,fy=factor)
      cv2.putText(img1,t,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
      cv2.putText(img1,t,(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
      img2=cv2.imread('dst/'+imgs[i+1])
      t=distances[predictDistance(img2)]
      factor = HEIGHT/img2.shape[0]
      img2 = cv2.resize(img2,(0,0),fx=factor,fy=factor)
      cv2.putText(img2,t,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
      cv2.putText(img2,t,(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
      printable=np.concatenate((img1,img2),axis=1)
      cv2.imwrite('../printables/printable_'+str(counter)+'.jpg',printable)
   else:
      printable=cv2.imread('dst/'+imgs[i])
      factor = HEIGHT/printable.shape[0]
      t=distances[predictDistance(printable)]
      printable = cv2.resize(printable,(0,0),fx=factor,fy=factor)
      cv2.putText(printable,t,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
      cv2.putText(printable,t,(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
      cv2.imwrite('../printables/printable_'+str(counter)+'.jpg',printable)
   counter+=1

