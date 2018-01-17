# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

import cv2
import sys
from facial_recognition import detect_faces
from screen import turnoff, turnon

if "__main__" == __name__:
	# Creating face cascade
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	# Set source to default webcam
	video_capture = cv2.VideoCapture(0)

	# detected face history
	faceHistory = []

	counter = 0
	
	while True:

		ret, frame = video_capture.read()
		# Only look at every third frame
		if counter % 3 == 0:

			faces, rect = detect_faces(frame)

			# Draw a rectangle around the faces
			if faces is not None:
				for (x, y, w, h) in rect:
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			# Turn off display if no faces found with a 5 frame requirement
			if not faces:
				faceHistory.append("off")
				if all(face == 'off' for face in faceHistory) and len(faceHistory) == 5:
					turnoff()
					faceHistory = []
			else:
				faceHistory.append("on")
				#if all(face == 'on' for face in faceHistory) and len(faceHistory) == 5:
				turnon()
				faceHistory = []

			# Display the resulting frame
			cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		counter += 1
	print("Exited.")
