import numpy as np
import cv2
import glob
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640,480)
'''
https://picamera.readthedocs.io/en/release-1.12/fov.html
resolutions to choose from:
1920,1080 <- recommended for high quality with low FoV
2592,1944 ?? probably not
1640,1232 <- recommended for highest quality and FoV
1640,922
1280,720
640,480
'''
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=camera.resolution)
# allow the camera to warmup
time.sleep(0.1)

# cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Frame', (640, 480))
i = 200

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	# show the frame
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame

	## FIND CHESS CORNERS
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	print("converted image to gray")
	ret, corners = cv2.findChessboardCorners(gray, (6,9), None)
	print("attempted to find chessboard")
	if ret == True:
		cv2.imwrite('test/cali_img_'+str(i)+'.jpg', image)
		print("attempted save image"+str(i))
		i += 1
		#draw chessboard
		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		image = cv2.drawChessboardCorners(image, (6,9), corners2, ret)

	image = cv2.resize(image, (640,480))
	cv2.imshow("Frame", image)
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
