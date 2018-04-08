#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import String
cap = cv2.VideoCapture(1)
x =360
flag1 = 0
area = 0
back = 1
def getArea() :
	move="nothing"
	global x,y,flag1,area,back
	[u,v] = [99,64]#[105, 117, 113]
	#flag1=True
	t=time.time()
	rec=True
	area1=0
	while rec:

		boln,f = cap.read()
		img_yuv = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)

		mask = cv2.inRange(img_yuv, (np.array([0,u-30,v-30])), (np.array([255,u+30,v+30])))

		erode = cv2.erode(mask,None,iterations = 1)
		dilate = cv2.dilate(erode,None,iterations = 1)
		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		if contour:
			cnt = max(contour, key = cv2.contourArea)		#getting contour with max area
			(x,y),radius = cv2.minEnclosingCircle(cnt)		#calculating center of the ball
			x,y,radius = int(x),int(y),int(radius)
			cv2.circle(f,(x,y),radius,(0,255,0),2)		#drawing circle across contour

			area = radius*radius*3.14
			

		
		if x>320+90 and back:
			move = "right"

		elif x<320-90 and back:
			move = "left"

		else:

			print "area",area
				#print "area1",area1
				#print area-area1
			if not flag1 and area<100000:
				move = "forward"
			elif area>100000 and flag1 == 0:
				flag1 = 2 
				move = "thresh"
			else:	
				back = 0
				move = "backward"

		if cv2.waitKey(1) == 27:
			break
		cv2.imshow("img",f)
		
		return move



def talker() :
	#msg=raw_input()
	pub=rospy.Publisher('get_area',String,queue_size=1)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(5)

	while not rospy.is_shutdown() :
		msg = getArea()
		print msg
		pub.publish(msg)
		time.sleep(0.1)

if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		pass

