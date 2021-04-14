import numpy as np
import cv2
from traffic import load_data


# img = cv2.imread('gtsrb-small/0/00000_00000.ppm',1)
# print(img)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

images, labels = load_data('gtsrb-small')

print(labels)
print(len(images)) # no of images
print(type(images[0])) # type of stored img
print(len(images[0])) # no of rows in 1st dim
print(len(images[0][0])) # no of pixel in each row
print(len(images[0][0][0])) # no of colors

img = images[0]
print('Original Dimensions : ',img.shape) 
dim = (30,30)
resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
cv2.imshow('image',resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print('Resized Dimensions : ',resized_img.shape) 
