import cv2
import sys
import threading

from recognizer import Recognizer
from screen import turnoff, turnon

class Viewer(object):
	"""docstring for Viewer"""
	def __init__(self, recognizer, subjects):
		super(Viewer, self).__init__()
		self.recognizer = recognizer
		self.video_capture = cv2.VideoCapture(0)
		self.subjects = subjects
		self.label_history = []
		self.counter = 0
		self.labels = []

		self.isRunning = False


	def processFrames(self):
		self.isRunning = True
		while True:
				# Only process every other frame to reduce CPU usage
				if self.counter % 2 == 0:
					ret, frame = self.video_capture.read()
					if frame is not None:
							recognized_face, labels, faces = self.recognizer.predict(self.subjects, frame)
							print(labels)
							print(self.counter)
							
							cv2.imshow('Face Recognizer', recognized_face)

							if labels and -1 not in labels:
								# Update face data every 300 frames
								if self.counter % 25 == 0 and len(labels) == 1:
									self.recognizer.update(faces, labels)

							# If face is unknown or no faces detected, turn off display
							if labels is None or -1 in labels:
								# Uses 5 frame buffer to have smoother transitions between on/off display
								self.label_history.append(-1)
								if len(self.label_history) == 10 and all(label == -1 for label in self.label_history):
									turnoff()
									self.label_history = []
							else:
								turnon()
								self.label_history = []

							if cv2.waitKey(1) & 0xFF == ord('q'):
								break
				self.counter += 1
		self.isRunning = False
		print("Exited.")

	def run(self):
		''' Threading to allow for frame processing in parallel with other functions '''
		t = threading.Thread(target=self.processFrames)
		t.start()


	def isRunning(self):
		return self.isRunning