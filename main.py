# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

import cv2
import sys
from facial_recognition import *
from screen import turnoff, turnon
from database import UsersDB

if "__main__" == __name__:


	db = UsersDB()
	training_data_path = "training-data/"
	db.new_user("Seth", "Y", training_data_path+"Seth/")
	db.new_user("Sam", "Y", training_data_path+"Sam/")
	db.new_user("Seth Rogen", "Y", training_data_path+"Seth Rogen/")
	print(db.query_all())
	

	subjects = db.query_subjects()
	subjects = dict(subjects)
	print(subjects)
	#train_save(db)
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	face_recognizer.read("LBPH_recognize_model.yml")
	video_capture = cv2.VideoCapture(0)


	label_history = []
	counter = 0
	while True:
		# Only process every other frame to reduce CPU usage
		if counter % 2 == 0:
			ret, frame = video_capture.read()
			if frame is not None:
					recognized_face, labels, faces = predict(face_recognizer, subjects, frame)
					print(labels)
					print(faces)
					cv2.imshow('Face Recognizer', recognized_face)
					
					#if labels:

						# Update face data every 300 frames
						#if counter % 300 == 0 and len(labels) == 1 and labels[0] != -1:
						#	update(labels, faces)

					# If face is unknown or no faces detected, turn off display
					if labels is None or -1 in labels:
						# Uses 5 frame buffer to have smoother transitions between on/off display
						label_history.append(-1)
						if len(label_history) == 10 and all(label == -1 for label in label_history):
							turnoff()
							label_history = []
					else:
						turnon()
						label_history = []

					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
		counter += 1
	print("Exited.")
