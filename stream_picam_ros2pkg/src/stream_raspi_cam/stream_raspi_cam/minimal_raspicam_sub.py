import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import copy
# import cv2
# from cv_bridge import CvBridge

class MinimalRaspicamPublisher(Node):
	def __init__(self):
		super().__init__("cam_pub")
		# init camera and grab ref to camera capture
		self.camera = PiCamera()
		self.camera.resolution = (1640,1232)
		self.camera.framerate = 30
		self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
		# allow time for camera to warm up
		time.sleep(1)

		self.img_pub_ = self.create_publisher(Image, "image_topic", 5)
		self.str_pub_ = self.create_publisher(String, "str_topic", 5)
		# self.bridge = CvBridge()
	
def main(args=None):
	rclpy.init(args=args)
	cam_pub = MinimalRaspicamPublisher()

	
	# cam_pub.get_logger().info("publishing image")
	# time.sleep(1)
	# print('before spin_once')
	# rclpy.spin_once(cam_pub, timeout_sec=0)
	# print('after spin_once')
	image_msg = Image()
	image_msg.height = 480
	image_msg.width = 640
	image_msg.encoding = 'rgb8'
	image_msg.is_bigendian = False # may need to check on this
	image_msg.step = 640*3
	image_msg.header.frame_id = 'raspi_cam'

	str_msg = String()
	str_msg.data = 'rpiprint'
	for frame in cam_pub.camera.capture_continuous(cam_pub.rawCapture, format='rgb', use_video_port=True):
		if rclpy.ok():
			_start = time.time()
			# image_msg.header.stamp = cam_pub.get_clock().now() TODO fix this
			data = frame.array.flatten()
			_grab_data = time.time()
			image_msg.data = data.tolist()
			_copy_data = time.time()
			cam_pub.img_pub_.publish(image_msg)
			# cam_pub.str_pub_.publish(str_msg)
			_publish_data = time.time()
			cam_pub.rawCapture.truncate(0)
			_truncate_data = time.time()
			rclpy.spin_once(cam_pub, timeout_sec=0)
			_end = time.time()
			print(_grab_data-_start, "\n", _copy_data-_start, "\n", _publish_data-_start, "\n", _truncate_data-_start, "\n", _end-_start, "\n")


if __name__ == '__main__':
	main()

