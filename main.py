# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

from recognizer import Recognizer
from viewer import Viewer
from database import UsersDB
from flask import Flask, render_template, Response, make_response
import time
import threading
import cv2


db = UsersDB()
training_data_path = "training-data/"
db.new_user("Seth", "Y", training_data_path+"Seth/")
db.new_user("Sam", "Y", training_data_path+"Sam/")
db.new_user("Seth Rogen", "Y", training_data_path+"Seth Rogen/")

subjects = db.query_subjects()
db.__del__()
subjects = dict(subjects)

recognizer = Recognizer()
viewer = Viewer(recognizer, subjects)
viewer.start()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def stream():
	print("streaming")

	frame = None
	global_frame = None
	while True:
		try:
			
			#_, img = viewer.video_capture.read()
			
			img = viewer.counter
			print(img)

			
			#cv2.imshow('Image before broadcast', img)

			#ret, jpeg = cv2.imencode('.jpg', img)
			#frame = jpeg.tobytes()

		except Exception as e:
			raise e
		'''finally:
			if frame != None:
				global_frame = frame
				viewer.cancel()
				yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

			else:
				yield (b'--frame\r\n'
	                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')'''
		


@app.route('/video_feed')
def video_feed():
	return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if "__main__" == __name__:

	app.run(debug=True, threaded=True)