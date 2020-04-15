# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import apriltag
import cv2

# init apriltag
# detector = apriltag.Detector()

# initialize the camera and grab a reference to the raw camera capture
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
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution)
# allow the camera to warmup
time.sleep(1)

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', camera.resolution)
# capture frames from the camera
i = 0
times = [0,0]
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	if times[1] != 0:
		timediff = times[0] - times[1]
		print("freq: ", 1/timediff)
		times[1] = times[0]
		times[0] = time.time()
	elif times[0] == 0:
		times[0] = time.time()
		print("updating time at 0")
	elif times[1] == 0:
		times[1] = time.time()
		print("updating time at 1")
	image = frame.array
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	if key == ord("s"):
		print("saved image_"+str(i)+".jpg")
		cv2.imwrite("image_"+str(i)+".jpg", image)
		i += 1