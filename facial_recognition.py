import cv2
import os
import numpy as np

def detect_faces(video_capture, faceCascade):
	# Capture frame
	ret, frame = video_capture.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize = (30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

	return faces, ret, frame



def add_face(label, numOfImages):
	# Add new face to face recognition collection
	if not os.path.isdir("training-data/" + label):
		os.makedirs("training-data/" + label)
		os.chdir("training-data/" + label)
		cam = cv2.VideoCapture(0)
		for i in range(numOfImages):
			s, img = cam.read()
			imwrite(label+i+".jpg", img)