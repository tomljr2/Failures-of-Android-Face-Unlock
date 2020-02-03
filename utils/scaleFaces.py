import cv2
from skimage.transform import rescale
from os import listdir
from os.path import isfile, join

HEIGHT=3264

# Get images from dst directory
imgs = [f for f in listdir('dst/') \
        if isfile(join('dst/', f))]

# Resize each image to be the same height
for imgpath in imgs:
   img = cv2.imread('dst/'+imgpath)
   factor = HEIGHT/img.shape[0]
   img = cv2.resize(img,(0,0),fx=factor,fy=factor)
   path=imgpath.split('.')
   cv2.imwrite('dst/'+path[0]+'.'+path[1],img)
