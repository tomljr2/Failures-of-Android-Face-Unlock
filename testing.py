from digitalRecords import records
from physicalRecords import records
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

MONITOR_WIDTH=2560.0
MONITOR_HEIGHT=1440.0

results=[]

# Function to test images digitally. This will display each image and then
# allow the user to input information about the person in the image.
def digitalTesting(same=True):
   # Get the images
   os.system('cd utils;python3 extractFaces.py;cd ..')
   imgs = [f for f in listdir('utils/dst/') if isfile(join('utils/dst/', f))]

   # Resize and display each image
   for img in imgs:
      image=cv2.imread('utils/dst/'+img)
      if image.shape[0] <= image.shape[1]:
         w=int(MONITOR_WIDTH)
         h=int(image.shape[0] *(MONITOR_WIDTH/image.shape[1]))
      else:
         w=int(image.shape[1] *(MONITOR_HEIGHT/image.shape[0]))
         h=int(MONITOR_HEIGHT)
      image2=cv2.resize(image,(w,h))
      cv2.imshow(img, image2)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      recordResults('digital',img,same,image)

def physicalTesting():
   dists=['Close (Front Camera)','Medium (Front Camera)','Far (Front Camera)', \
          'Close (Back Camera)','Medium (Back Camera)','Far (Back Camera)']
   for d in dists:
      print(d)
      print()
      recordResults('physical',None,True,None,d)
   return

# Record the results for different resolutions, distances, sexes,
# ages, races, and nationalities.
def recordResults(name,img,same,image=None,d=None):
   os.system('cp '+name+'Records.py ./backup/'+name+'Backup.py')
   f=open(name+'Records.py','w')

   succ=int(input('Number of successes: '))
   # If something was extracted as a face, but is wrong, then
   # we can just enter an invalid number of successes to get
   # rid of that picture
   if succ > 10 or succ < 0:
      if name=='digital':
         os.system('rm utils/dst/'+img)
      f.write('records='+str(records))
      f.close()
      return
   if d == None:
      d=getDistance(image)

   # If it's the same person, there's no need to repeat questions
   if not same:
      s=getSex()
      a=getAge()
      r=getRace()
      print()
      n=input('Nationality: ')
   if not results and same:
      results.append(getSex())
      results.append(getAge())
      results.append(getRace())
      print()
      results.append(input('Nationality: '))
   if same:
      s=results[0]
      a=results[1]
      r=results[2]
      n=results[3]
   print()

   addRecord(succ,'Totals')
   addRecord(succ,(d,s,a,r,n))
   addRecord(succ,d)
   addRecord(succ,s)
   addRecord(succ,a)
   addRecord(succ,r)
   addRecord(succ,n)

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
   ages=['0-4 years','5-9 years','10-14 years','15-19 years', \
         '20-24 years','25-29 years','30-39 years','40-49 years', \
         '50-59 years','60-69 years','70-79 years','80+ years']
   print()
   for i in range(1,13):
      print(str(i)+'. '+ages[i-1])
   r=int(input('Age Group: '))
   return ages[r-1]

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
      print('Expected choice: '+str(np.argmin(np.power(res,2))+1))

def mainMenu():
   print('1. Digital Testing (Same person)')
   print('2. Digital Testing (Multiple people)')
   print('3. Physical Testing (Same person)')
   print('4. Generate printables')
   print('5. Quit')
   x=int(input('Choice: '))
   if x==1:
      digitalTesting()
   elif x==2:
      digitalTesting(False)
   elif x==3:
      physicalTesting()
   elif x==4:
      os.system('cd utils;python3 physicalTesting.py;cd ..;')

mainMenu()
