import cv2
import sys
from threading import Thread, Lock
from time import sleep

from recognizer import Recognizer
from screen import turnoff, turnon

class Viewer(Thread):
	"""docstring for Viewer"""
	def __init__(self, recognizer, subjects):
		super(Viewer, self).__init__()
		self.recognizer = recognizer
		self.video_capture = cv2.VideoCapture(0)
		self.subjects = subjects
		self.label_history = []
		self.counter = 0
		self.labels = []


		# Status variables
		self.daemon = False
		self.currentFrame = None
		self.isRunning = False
		self.screen = True
		self.unauthorizedDetected = False



	def run(self):
		''' Threading to allow for frame processing in parallel with other functions '''
		
		self.isRunning = True
		while self.isRunning:
			self.currentFrame = self.processFrame()
			self.counter += 1
			#print(self.currentFrame)
			sleep(1)
		print("Exited.")


	def processFrame(self):
		# Only process every other frame to reduce CPU usage
		if self.counter % 2 == 0:
			ret, frame = self.video_capture.read()
			if frame is not None:
					recognized_face, self.labels, faces = self.recognizer.predict(self.subjects, frame)
					returnFrame = recognized_face[:]
					cv2.imshow('Face Recognizer', recognized_face)

					# If face is unknown or no faces detected, turn off display
					if self.labels is None or -1 in self.labels:
						# Uses 5 frame buffer to have smoother transitions between on/off display
						self.label_history.append(-1)
						if len(self.label_history) == 10 and all(label == -1 for label in self.label_history):
							turnoff()
							self.screen = False
							self.label_history = []
							self.unauthorizedDetected = True
					else:
						turnon()
						self.screen = True
						self.label_history = []
						self.unauthorizedDetected = False
						# Update face data every 300 frames
						#if self.counter % 25 == 0 and len(self.labels) == 1:
							#self.recognizer.update(faces, self.labels)
					return returnFrame

	def cancel(self):
		''' End the thread '''
		self.isRunning = False

	
	#def setCurrentFrame(self, value):
#