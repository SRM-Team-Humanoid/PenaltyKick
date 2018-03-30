#!/usr/bin/env python
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import Bool

try:
	index = sys.argv[1]
except:
	index = 0 



cap = cv2.VideoCapture(index)

y,u,v = 0,62,215
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
		
		ret,frame = cap.read()

		img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
		mask = cv2.inRange(img_yuv, (np.array([0,u-25,v-25])), (np.array([255,u+25,v+25])))

		
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
			cv2.circle(frame,(x,y),radius,(0,255,0),2)		#drawing circle across contour

			area = radius*radius*3.14
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)
          		#return True
			if area:
				#print "detected"

				return True
			'''
			else:
				return "not in range"
			
		
			print "area: ",area," ","x: ",x," ","y: ",y	
			'''

		else:
			#print "Not detected"
			#print "Contour Nahi He				
			cv2.imshow("Masking",mask)
			cv2.imshow("YUV",frame)
			return False
		

	


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





