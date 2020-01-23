import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
os.system('cd utils;python3 extractAndScaleFaces.py;cd ..')

imgs = [f for f in listdir('utils/dst/') if isfile(join('utils/dst/', f))]

counter=1
for i in range(0,len(imgs),2):
   if i+1 < len(imgs):
      img1=cv2.imread('utils/dst/'+imgs[i])
      img2=cv2.imread('utils/dst/'+imgs[i+1])
      printable=np.concatenate((img1,img2),axis=1)
      cv2.imwrite('printables/printable_'+str(counter)+'.jpg',printable)
   else:
      printable=cv2.imread('utils/dst/'+imgs[i])
      cv2.imwrite('printables/printable_'+str(counter)+'.jpg',printable)
   counter+=1

