import cv2
import sys
from threading import Thread, Lock
from time import sleep

from recognizer import Recognizer
from screen import turnoff, turnon


video_capture = cv2.VideoCapture(0)
#subjects = subjects
label_history = []
#counter = 0
labels = []
screen = True

# Status variables
daemon = False
currentFrame = None
isRunning = False
screen = True
unauthorizedDetected = False



def processFrame(recognizer, counter, subjects):
  # Only process every other frame to reduce CPU usage
  global label_history
  global labels
  global screen
  if counter % 2 == 0:
    ret, frame = video_capture.read()
    if frame is not None:
        recognized_face, labels, faces = recognizer.predict(subjects, frame)
        returnFrame = recognized_face

        # If face is unknown or no faces detected, turn off display
        if labels is None or -1 in labels:
          # Uses 5 frame buffer to have smoother transitions between on/off display
          label_history.append(-1)
          if len(label_history) == 10 and all(label == -1 for label in label_history):
            turnoff()
            screen = False
            label_history = []
            unauthorizedDetected = True
        else:
          turnon()
          screen = True
          label_history = []
          unauthorizedDetected = False
          # Update face data every 300 frames
          #if self.counter % 25 == 0 and len(self.labels) == 1:
            #self.recognizer.update(faces, self.labels)
        return returnFrame
    return "Borked"