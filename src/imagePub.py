#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import Bool

try:
	index = sys.argv[1]
except:
	index = 1 



cap = cv2.VideoCapture(index)

y,u,v = 0,99,50
kernel = np.ones((5,5),np.uint8)

width = cap.get(3)
height= cap.get(4)
area = 0
flag = 1
print width
print height

state = 0
#cv2.namedWindow("Masking")
#cv2.namedWindow("YUV")
def detect():

	global cap,y,u,v,kernel,width,height,flag,area
	
	while flag:
		
		ret,frame = cap.read()

		img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
		mask = cv2.inRange(img_yuv, (np.array([0,u-45,v-45])), (np.array([255,u+45,v+45])))

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)	

		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		if cv2.waitKey(1) == 27:
			flag = 0
		 

		
		if contour:
			#cnt = contour[0]
			cnt = max(contour, key = cv2.contourArea)		#getting contour with max area
			(x,y),radius = cv2.minEnclosingCircle(cnt)		#calculating center of the ball
			x,y,radius = int(x),int(y),int(radius)
			cv2.circle(frame,(x,y),radius,(0,455,0),2)		#drawing circle across contour

			area = radius*radius*3.14
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)

			if area:
				x1,y1 = width/2,height/2
				print x1,x
				print y1,y

				param = 100

				if state == 0:
					state = 1
					return "stop"
				if state == 1:
					state = 2
					return "balance"

				if state == 2:
					state = 3
					return "move_f"
				if state == 3:
					state = 0
					return "kick"
					


		else:
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)
			
			if state == 0:
				return "pan"
			if state == 1:
				return "side"
			if state == 2:
				return "tilt_d"
			if state == 3:
				return "align"


		

	


def talker() :

	pub=rospy.Publisher('detect',Bool,queue_size=10)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		msg = detect()
		pub.publish(msg)


if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		cap.release()
		cv2.destroyAllWindows()





