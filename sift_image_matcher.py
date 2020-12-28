import sys
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
try:
	img1 = cv.imread(sys.argv[1],cv.IMREAD_GRAYSCALE)          # queryImage
except:
	sys.exit(1)
try:
	img2 = cv.imread(sys.argv[2],cv.IMREAD_GRAYSCALE) # trainImage
except:
	sys.exit(1)

if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(1)

# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
print len(good)
sys.exit(0)
# cv.drawMatchesKnn expects list of lists as matches.
#img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#plt.imshow(img3),plt.show()
