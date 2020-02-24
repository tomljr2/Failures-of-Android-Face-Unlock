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
      h3 = int(h*0.3)
      path=imgpath.split('.')
      print(i)
      face = img[y-h3:y+h+h2,x-w2:x+w+w2]
      if face.shape[0] > 0 and face.shape[1] > 0:
         cv2.imwrite('dst/'+path[0]+'_'+str(i)+'.'+path[1], \
                    face)
      else:
         cv2.imwrite('dst/'+path[0]+'_'+str(i)+'.'+path[1], \
                    img[y:y+h,x:x+w])
         print('Error')
      i+=1


   if i==1:
      cv2.imwrite('dst/'+imgpath.split('.')[0]+'_'+str(i)+'.'+path[1], \
                    img)
