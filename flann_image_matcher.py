import sys
import numpy as np
import cv2 
#from matplotlib import pyplot as plt


try:

	img1 = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)          # queryImage
except:
	sys.exit(1)
try:
	img2 = cv2.imread(sys.argv[2],cv2.IMREAD_GRAYSCALE) # trainImage
except:
	sys.exit(1)

if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(1)

# Initiate SIFT detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

des1 = np.float32(des1)
des2 = np.float32(des2)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

matchesCount = 0 


# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
 # print i
  if m.distance < 0.7*n.distance:
    matchesMask[i]=[1,0]
    
    #print i
    matchesCount = matchesCount + 1

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

#if 0 < matchesCount:
#  img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
#  plt.imshow(img3,),plt.show()
print matchesCount
sys.exit(0)
#sys.exit(matchesCount)
