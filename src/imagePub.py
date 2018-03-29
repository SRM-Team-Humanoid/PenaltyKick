#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import String

try:
	index = sys.argv[1]
except:
	index = 0



cap = cv2.VideoCapture(index)

y,u,v = 0,124,68
kernel = np.ones((5,5),np.uint8)

width = cap.get(3)
height= cap.get(4)
area = 0
flag = 1
#cv2.namedWindow("Masking")
#cv2.namedWindow("YUV")
def detect():

	global cap,y,u,v,kernel,width,height,flag,area
	
	while flag:
		#get_image
		ret,frame = cap.read()

		#colour space conversion and masking
		img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
		mask = cv2.inRange(img_yuv, (np.array([0,u-25,v-25])), (np.array([255,u+25,v+25])))

		#morphological_transformation_open
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)

		#morphological_transformation_close
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)	

		#contour detection
		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		#cv2.drawContours(frame, contour, -1, (0,255,0), 2)
		
		#waitKey init
		if cv2.waitKey(5) == 27:
			flag = 0 

		#contour operations
		if contour:
			#cnt = contour[0]
			cnt = max(contour, key = cv2.contourArea)		#getting contour with max area
			(x,y),radius = cv2.minEnclosingCircle(cnt)		#calculating center of the ball
			x,y,radius = int(x),int(y),int(radius)
			cv2.circle(frame,(x,y),radius,(0,255,0),2)		#drawing circle across contour

			area = radius*radius*3.14
          
			if area>1000:
				return "detected"

			else:
				return "not in range"
			

			#print "area: ",area," ","x: ",x," ","y: ",y	


		else:

			return "not"
			#print "Contour Nahi He"

					
		cv2.imshow("Masking",mask)
		cv2.imshow("YUV",frame)
		

	cap.release()
	cv2.destroyAllWindows()


def talker() :

	pub=rospy.Publisher('detect',String,queue_size=10)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		msg = detect()
		pub.publish(msg)


if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		pass






