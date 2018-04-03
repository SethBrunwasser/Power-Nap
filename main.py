# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

import cv2
import sys
from recognizer import Recognizer
from screen import turnoff, turnon
from viewer import Viewer
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
	recognizer = Recognizer()
	video_capture = cv2.VideoCapture(0)
	viewer = Viewer(recognizer, subjects)
	viewer.run()
