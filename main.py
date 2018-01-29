# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

import cv2
import sys
from facial_recognition import *
from screen import turnoff, turnon
from database import UsersDB

if "__main__" == __name__:

	subjects = {-1: "Unknown", 1: "Seth", 2: "Sam", 3:"Seth Rogen"}
	#train_save()
	#face_recognizer = cv2.face.FisherFaceRecognizer_create()
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	face_recognizer.read("LBPH_recognize_model.yml")
	video_capture = cv2.VideoCapture(0)

	training_data_path = "training-data/"

	db = UsersDB()
	db.new_user("Sam", "Y", training_data_path+"Sam/")
	db.new_user("Seth", "Y", training_data_path+"Seth/")
	db.new_user("Seth Rogen", "Y", training_data_path+"Seth Rogen/")
	print(db.query_all())
	
	label_history = []
	counter = 0
	while True:
		# Only process every other frame to reduce CPU usage
		if counter % 2 == 0:
			ret, frame = video_capture.read()
			if frame is not None:
					recognized_face, label = predict(face_recognizer, subjects, frame)
					cv2.imshow('Face Recognizer', recognized_face)
					
					# If face is unknown, turn off display
					if label:
						if label == -1:
							# Uses 5 frame buffer to have smoother transitions between on/off display
							label_history.append(label)
							if len(label_history) == 20 and all(label == -1 for label in label_history):
								turnoff()
								label_history = []
						else:
							turnon()

					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
		counter += 1
	print("Exited.")
