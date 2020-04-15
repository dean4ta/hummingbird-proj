import numpy as np
import numpy.random as npr
import cv2
import glob
import argparse

HEADLESS = True

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('test/*.jpg')
image_template = cv2.imread(images[0])
gray = cv2.cvtColor(image_template, cv2.COLOR_BGR2GRAY) # initializing variable outside of for loop scope

for i in range(len(images)):
    print('finding chess pattern in '+fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (6,9),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print('found it')
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        if not HEADLESS:
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (6,9), corners2,ret)
            cv2.imshow('img',img)
            cv2.waitKey(500)
        # if len(objpoints) >= 10:
        #     break

if not HEADLESS:
    cv2.destroyAllWindows()

print('calibrating camera on '+str(len(images))+'...')
print(len(objpoints))
print(len(imgpoints))
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print(ret)
print(mtx)
print(dist)
print(rvecs)
print(tvecs)

