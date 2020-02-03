import cv2
from os import listdir
from os.path import isfile, join

# Import the cv2 trained face classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + \
                                     'haarcascade_frontalface_default.xml')

# Get all of the images from the src/ directory
imgs = [f for f in listdir('../src_images/') \
        if isfile(join('../src_images/', f))]

# Loop over each image
for imgpath in imgs:
   # Read the images and detect any faces
   img=cv2.imread('../src_images/'+imgpath)
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   faces = face_cascade.detectMultiScale(gray, 1.3, 5)

   # Extract each face and save to the dst/ directory
   i=1
   for (x,y,w,h) in faces:
      w2 = int(w*0.1)
      h2 = int(h*0.15)
      path=imgpath.split('.')
      face = img[y-3*h2:y+h+h2,x-w2:x+w+w2]
      cv2.imwrite('dst/'+path[0]+'_'+str(i)+'.'+path[1], \
                 face)
      i+=1
