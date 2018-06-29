# If no faces are found, then the display will sleep.
# If a face is found, then the monitor will wake.

# Press Q to exit

from recognizer import Recognizer
from database import UsersDB
from flask import Flask, render_template, Response, make_response
from multiprocessing import Process
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
#viewer.start()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def stream():

	frame = None
	global_frame = None
	prev = None
	counter = 0
	from viewer import processFrame as pf
	print("streaming")

	
	while True:
		try:
			

			#_, img = viewer.video_capture.read()
			#threading.lock.acquire()
			#img = viewer.currentFrame
			#threading.lock.release()
			#print(img)

			
			#cv2.imshow('Image before broadcast', img)
			img = pf(recognizer, counter, subjects)

			#print(img)
			counter += 1
			#print("Counter:\t" + str(counter))
			#print("Img:\t\t" + str(img))
			if img is not None:
				ret, jpeg = cv2.imencode('.jpg', img)
				prev = jpeg
				frame = jpeg.tobytes()
			else:
				frame = prev.tobytes()
			
		except Exception as e:
			raise e
		finally:
			if frame != None:
				global_frame = frame
				yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
			else:
				yield (b'--frame\r\n'
	                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
		

@app.route('/video_feed')
def video_feed():
	return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if "__main__" == __name__:
	p = Process(target=stream)
	p.start()
	app.run(debug=True, use_reloader=False)
	p.join()
