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

	# Save last 100 faces
	faceHistory = []
	while True:
		faces, ret, frame = detect_faces(video_capture=video_capture, faceCascade=faceCascade)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		# Turn off display if no faces found with a 5 frame requirement
		if len(faces) == 0:
			faceHistory.append("off")
			if all(face == 'off' for face in faceHistory) and len(faceHistory) == 5:
				turnoff()
				faceHistory = []
		else:
			faceHistory.append("on")
			#if all(face == 'on' for face in faceHistory) and len(faceHistory) == 5:
			turnon()
			faceHistory = []

	print("Exited.")