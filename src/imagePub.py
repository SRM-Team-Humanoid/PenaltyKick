mport cv2
import numpy as np
import time
import rospy
from std_msgs.msg import String


try:
	index = sys.argv[1]
except:
	index = 1 



cap = cv2.VideoCapture(index)

u,v = 99,64
kernel = np.ones((5,5),np.uint8)

width = cap.get(3)
height= cap.get(4)

cap.set(3,width/3)
cap.set(4,height/3)

flag1=0
area = 0
state = 0
back = 1
stop = False
x,y = 0,0

cv2.namedWindow("YUV")
paramx,paramy = 50,50


x1,y1 = int(width/2),int(height/2)


def detect():

	global cap,y,u,v,kernel,width,height,flag,area,state,paramx,paramy,x1,y1,stop
	
	while True:
		
		ret,frame = cap.read()

		img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
		mask = cv2.inRange(img_yuv, (np.array([0,u-30,v-30])), (np.array([255,u+30,v+30])))

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)

		
		erode = cv2.erode(mask,kernel,iterations = 1)
		dilate = cv2.dilate(erode,kernel,iterations = 1)	

		image,contour,hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		if cv2.waitKey(1) == 27:
			flag = 0
		 
		#cv2.rectangle(frame,(x1-paramx,y1-paramy),(x1+paramx,y1+paramy),(0,255,0),3)
		
		if contour:
			cnt = max(contour, key = cv2.contourArea)		
			(x,y),radius = cv2.minEnclosingCircle(cnt)		
			x,y,radius = int(x),int(y),int(radius)
			#cv2.circle(frame,(x,y),radius,(0,455,0),2)		
			#area = radius*radius*3.14
			#cv2.imshow("YUV",frame)
			
			if x<x1+paramx and x>x1-paramx and y<y1+paramy and y>y1-paramy:
				if state == 0:
					state = 1
					return "stop"
				if state == 1:
					print "state1"
					stop = True
			else :
				if state == 0:
					return "pan"
				if state == 1:
					return "side"
				
					state = 2
					#return "sleep"

				if state == 2:					
					return "move_f"
				
			else:
				if state == 0:
					return "pan"
				if state == 1:
					if X<x1+param and x>x1-param:
						if y>y1+param:
							return "tilt_u"
						elif y<y1-param:
							return "tilt_d"
					else:
						return "side"

				if state ==2:
					state = 1

		else:
			cv2.imshow("YUV",frame)
			if state == 0:
				return "pan"
			if state == 1:
				return "side"
		
			if state == 2:
				state = 0


def getArea() :

	move="nothing"
	global x,y,flag1,area,back
	[u,v] = [99,64]
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
			cnt = max(contour, key = cv2.contourArea)		
			(x,y),radius = cv2.minEnclosingCircle(cnt)		
			x,y,radius = int(x),int(y),int(radius)
			cv2.circle(f,(x,y),radius,(0,255,0),2)		
			area = radius*radius*3.14
			

		print area
		if x>320+90 and back:
			move = "right"

		elif x<320-90 and back:
			move = "left"

		elif y>390 :
			move = "tilt_d"

		else:

			if area<20000:
				move = "forward"
			else:
				move = "thresh"

		if cv2.waitKey(1) == 27:
			break
		
		return move

	


def talker() :
	global stop
	pub=rospy.Publisher('detect',String,queue_size=1)
	rospy.init_node('talker',anonymous=True) 
	rate=rospy.Rate(10)

	while not rospy.is_shutdown() :
		if not stop:
		
			msg = detect()
		else:
		
			msg = getArea()

		pub.publish(msg)


if __name__=="__main__" :
	try :
		talker()
	except rospy.ROSInterruptException :
		cap.release()
		cv2.destroyAllWindows()







