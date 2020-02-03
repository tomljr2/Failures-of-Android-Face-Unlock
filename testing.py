from records import records
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

MONITOR_WIDTH=2560
MONITOR_HEIGHT=1440

# Function to test images digitally. This will display each image and then
# allow the user to input information about the person in the image.
def digitalTesting():
   # Get the images
   os.system('cd utils;python3 extractFaces.py;cd ..')
   imgs = [f for f in listdir('utils/dst/') if isfile(join('utils/dst/', f))]

   # Resize and display each image
   for img in imgs:
      image=cv2.imread('utils/dst/'+img)
      if image.shape[0] <= image.shape[1]:
         w=MONITOR_WIDTH
         h=int(image.shape[0] *(MONITOR_WIDTH/image.shape[1]))
      else:
         w=int(image.shape[1] *(MONITOR_HEIGHT/image.shape[0]))
         h=MONITOR_HEIGHT
      image2=cv2.resize(image,(w,h))
      cv2.imshow(img, image2)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      succ=-1
      while succ > 10 or succ < 0:
         succ=int(input('Number of successes: '))
         if succ > 10 or succ < 0:
            print('Error: Must be a number from 0 to 10')
      d=getDistance(image)
      s=getSex()
      a=getAge()
      r=getRace()
      print()
      n=input('Nationality: ')
      recordResults(w,h,d,s,a,r,n,succ)
      print()

# Record the results for different resolutions, distances, sexes,
# ages, races, and nationalities.
def recordResults(w,h,dist,s,age,race,nat,succ):
   os.system('cp records.py ./backup/backup.py')
   f=open('records.py','w')
   addRecord(succ,'Totals')
   addRecord(succ,(w,h,dist,s,age,race,nat))
   addRecord(succ,dist)
   addRecord(succ,s)
   addRecord(succ,age)
   addRecord(succ,race)
   addRecord(succ,nat)
   f.write('records='+str(records))
   f.close()

def addRecord(succ,idx):
   try:
      if succ !=0:
         records[idx][0]+=succ
         records[idx][1]+=10
         records[idx][2]=records[idx][0]/records[idx][1]
   except:
         records[idx]=[succ,10,succ/10]

# Functions to display a menu to enter information about a person
def getRace():
   races=['American Indian or Alaska Native','Asian', \
          'Black or African American','Hispanic or Latino', \
          'Native Hawaiian or Other Pacific Islander','White']
   print()
   for i in range(1,7):
      print(str(i)+'. '+races[i-1])
   r = int(input('Race: '))
   return races[r-1]

def getSex():
   sexes=['Male','Female']
   print()
   for i in range(1,3):
      print(str(i)+'. '+sexes[i-1])
   r=int(input('Sex: '))
   return sexes[r-1]

def getDistance(img):
   dists=['Close (Front Camera)','Medium (Front Camera)','Far (Front Camera)', \
          'Close (Back Camera)','Medium (Back Camera)','Far (Back Camera)']
   print()
   for i in range(1,7):
      print(str(i)+'. '+dists[i-1])
   predictDistance(img)
   r=int(input('Distance: '))
   return dists[r-1]

def getAge():
   ages=['0 years','1-4 years','5-9 years','10-14 years','15-19 years', \
         '20-24 years','25-29 years','30-34 years','35-39 years','40-44 years', \
         '45-49 years','50-54 years','55-59 years','60-64 years','65-69 years', \
         '70-74 years','75-79 years','80-84 years','85+ years']
   print()
   for i in range(1,20):
      print(str(i)+'. '+ages[i-1])
   r=int(input('Age Group: '))
   return ages[r-1]

# Function to predict the distance based on the resolution
def predictDistance(img):
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
   print('Expected choice: '+str(np.argmin(np.power(res,2))+1))
digitalTesting()
