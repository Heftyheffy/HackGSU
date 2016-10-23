from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from Compare import getCompare

def runDexter():
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help="path to the (optional) video file")
	ap.add_argument("-b", "--buffer", type=int, default=32,
		help="max buffer size")
	args = vars(ap.parse_args())

	
	#blueLower = (86, 31, 4)
	#blueUpper = (220, 88, 50)
	blueUpper = (150, 255, 200)
	blueLower = (100, 50, 50)
	#redLower = (40, 40, 150)
	#redUpper = (80, 80, 245)
	redLower = (150,70,50)
	redUpper = (200, 255, 200)
	
	pts = deque(maxlen=args["buffer"])
	pts2 = deque(maxlen=args["buffer"])
	counter = 0
	(dX, dY) = (0, 0)
	direction = ""

	if not args.get("video", False):
		camera = cv2.VideoCapture(0)

	else:
		camera = cv2.VideoCapture(args["video"])

	centerX = 0
	centerY = 0
	center2X = 0
	center2Y = 0
		
	shirtIsIn = False
	canIsIn = True

	while True:

		(grabbed, frame) = camera.read()

		if args.get("video") and not grabbed:
			break

		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(hsv, blueLower, blueUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		
		mask2 = cv2.inRange(hsv, redLower, redUpper)
		mask2 = cv2.erode(mask2, None, iterations=2)
		mask2 = cv2.dilate(mask2, None, iterations=2)

		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		center2 = None
		radius = 0
		
		if len(cnts) > 0:

			c = max(cnts, key=cv2.contourArea)

			if(shirtIsIn == False and getCompare(c, 1) < .2):
				shirtIsIn = True
				print 'shirtIsIn'
				
			if(shirtIsIn):
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				centerX = int(M["m10"] / M["m00"])
				centerY = int(M["m01"] / M["m00"])
				center = (centerX, centerY)
				
				with open('shirt.txt', 'w') as f:
					f.write('\n' + str(centerX))


				if centerX < 5 or centerX > 580 or centerY > 440 or centerY < 10:
					s = "dx: ", centerX, ', dy: ', centerY
				
			isOnScreen = True
			
			 
			try:
				c2 = max(cnts2, key=cv2.contourArea)
				
				if(canIsIn == False and getCompare(c2, 0) < 100):
					canIsIn = True
					print 'canIsIn'
			except:
				isOnScreen = False
				
			if isOnScreen and canIsIn:
				M2 = cv2.moments(c2)
				center2X = int(M2["m10"] / M2["m00"])
				center2Y = int(M2["m01"] / M2["m00"])
				center2 = (center2X, center2Y )
							
				with open('cup.txt', 'w') as f:
					f.write('\n' + str(center2X))
				
				if centerX < 5 or centerX > 580 or centerY > 440 or centerY < 10:
					s = "dx: ", center2X, ', dy: ', center2Y
					
				if radius > 10:

					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					pts.appendleft(center)
					
					cv2.circle(frame, center2, 5, (0, 0, 255), -1)
					pts.appendleft(center2)

		for i in np.arange(1, len(pts)):

			if pts[i - 1] is None or pts[i] is None:
				continue
			try:
				a = pts[-10]
			except:
				continue

			if counter >= 10 and i == 1 and pts[-10] is not None:

				dX = pts[-10][0] - pts[i][0]
				dY = pts[-10][1] - pts[i][1]
				(dirX, dirY) = ("", "")
				
		cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 3)
		cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.35, (0, 0, 255), 1)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		counter += 1

		if key == ord("q"):
			break

	camera.release()
	cv2.destroyAllWindows()
runDexter()