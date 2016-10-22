# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
blueLower = (100, 50, 50)
blueUpper = (150, 255, 200)

redLower = (150, 70, 50)
redUpper = (200, 255, 200)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
pts2 = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, blueLower, blueUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	mask2 = cv2.inRange(hsv, redLower, redUpper)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	center2 = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)		
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		centerX = int(M["m10"] / M["m00"])
		centerY = int(M["m01"] / M["m00"])
		center = (centerX, centerY)
		cv2.drawContours(frame,c,-1,(0,255,0),3)

		if centerX < 5 or centerX > 580 or centerY > 440 or centerY < 10:
			s = "dx: ", centerX, ', dy: ', centerY
			print s
			
		isOnScreen = True
		 
		try:
			c2 = max(cnts2, key=cv2.contourArea)
		except:
			isOnScreen = False
		if isOnScreen:
			M2 = cv2.moments(c2)
			center2X = int(M2["m10"] / M2["m00"])
			center2Y = int(M2["m01"] / M2["m00"])
			center2 = (center2X, center2Y )
			cv2.drawContours(frame,c2,-1,(0,255,0),3)
			
			if centerX < 5 or centerX > 580 or centerY > 440 or centerY < 10:
				s = "dx: ", center2X, ', dy: ', center2Y
				print s
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points

				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				pts.appendleft(center)
				
				cv2.circle(frame, center2, 5, (0, 0, 255), -1)
				pts.appendleft(center2)

	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		try:
			a = pts[-10]
		except:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
			


		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		#thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		#cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		#cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()