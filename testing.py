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
   os.system('cd utils;python3 extractAndScaleFaces.py;cd ..')
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
      image=cv2.resize(image,(w,h))
      cv2.imshow('Digital Testing', image)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      succ=-1
      while succ > 10 or succ < 0:
         succ=int(input('Number of successes: '))
         if succ > 10 or succ < 0:
            print('Error: Must be a number from 0 to 10')
      d=getDistance()
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
   print()
   print('1. American Indian or Alaska Native')
   print('2. Asian')
   print('3. Black or African American')
   print('4. Hispanic or Latino')
   print('5. Native Hawaiian or Other Pacific Islander')
   print('6. White')
   r = int(input('Race: '))
   if r==1:
      return 'American Indian or Alaska Native'
   elif r==2:
      return 'Asian'
   elif r==3:
      return 'Black or African American'
   elif r==4:
      return 'Hispanic or Latino'
   elif r==5:
      return 'Native Hawaiian or Other Pacific Islander'
   else:
      return 'White'

def getSex():
   print()
   print('1. Male')
   print('2. Female')
   r=int(input('Sex: '))
   if r==1:
      return 'Male'
   else:
      return 'Female'

def getDistance():
   print()
   print('1. Close (Front Camera)')
   print('2. Medium (Front Camera)')
   print('3. Far (Front Camera)')
   print('4. Close (Back Camera)')
   print('5. Medium (Back Camera)')
   print('6. Far (Back Camera)')
   r=int(input('Distance: '))
   if r==1:
      return 'Close (Front Camera)'
   elif r==2:
      return 'Medium (Front Camera)'
   elif r==3:
      return 'Far (Front Camera)'
   elif r==4:
      return 'Close (Back Camera)'
   elif r==5:
      return 'Medium (Back Camera)'
   else:
      return 'Far (Back Camera)'

def getAge():
   print()
   print('1. 0 years')
   print('2. 1-4 years')
   print('3. 5-9 years')
   print('4. 10-14 years')
   print('5. 15-19 years')
   print('6. 20-24 years')
   print('7. 25-29 years')
   print('8. 30-34 years')
   print('9. 35-39 years')
   print('10. 40-44 years')
   print('11. 45-49 years')
   print('12. 50-54 years')
   print('13. 55-59 years')
   print('14. 60-64 years')
   print('15. 65-69 years')
   print('16. 70-74 years')
   print('17. 75-79 years')
   print('18. 80-84 years')
   print('19. 85+ years')
   r=int(input('Age Group: '))
   if r==1:
      return '0 years'
   elif r==2:
      return '1-4 years'
   elif r==3:
      return '5-9 years'
   elif r==4:
      return '10-14 years'
   elif r==5:
      return '15-19 years'
   elif r==6:
      return '20-24 years'
   elif r==7:
      return '25-29 years'
   elif r==8:
      return '30-34 years'
   elif r==9:
      return '35-39 years'
   elif r==10:
      return '40-44 years'
   elif r==11:
      return '45-49 years'
   elif r==12:
      return '50-54 years'
   elif r==13:
      return '55-59 years'
   elif r==14:
      return '60-64 years'
   elif r==15:
      return '65-69 years'
   elif r==16:
      return '70-74 years'
   elif r==17:
      return '75-79 years'
   elif r==18:
      return '80-84 years'
   else:
      return '85+ years'

digitalTesting()
