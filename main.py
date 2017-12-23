# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.
import cv2
import sys
from facial_recognition import faces
from screen import turnoff, turnon

if "__main__" == __name__:
	# Creating face cascade
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	# Set source to default webcam
	video_capture = cv2.VideoCapture(0)

	# Save last 100 faces
	faceHistory = 0
	while True:
		faces, ret, frame = faces(video_capture=video_capture, faceCascade=faceCascade)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		# Turn off display if no faces found
		if not faces:
			faceHistory += 1
			if faceHistory == 100:
				turnoff()
		else:
			turnon()

	print("Exited.")
