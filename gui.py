import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color
from kivy.graphics import Canvas
from kivy.graphics import Rectangle

import cv2
import numpy as np
from facial_recognition import detect_faces
from screen import turnoff, turnon



class PowerNapApp(App):

	def build(self):
		self.img1 = Image(source='images/1.jpg')
		layout = BoxLayout(orientation='vertical', spacing=0)
		layout.add_widget(videoPanelWidget(self.img1))
		btn1 = Button(text='Hello')

		options = BoxLayout(orientation='vertical')
		options.add_widget(Button(text='Hello'))
		options.add_widget(Button(text='Hello'))
		options.add_widget(Button(text='Hello'))
		layout.add_widget(options)
		
		#opencv2 stuffs
		self.capture = cv2.VideoCapture(0)
		ret, frame = self.capture.read()
		#cv2.namedWindow("CV2 Image")
		#cv2.imshow("CV2 Image", frame)
		Clock.schedule_interval(self.update, 1.0/33.0)
		return layout

	def CreateImage(self, height, width, bits=np.uint8, channels=3, color=(0, 0, 0)): # (cv.GetSize(frame), 8, 3)
		"""Create new image(numpy array) filled with certain color in RGB"""
		# Create black blank image

		if bits == 8:
			bits = np.uint8
		elif bits == 32:
			bits = np.float32
		elif bits == 64:
			bits = np.float64
		image = np.zeros((height, width, channels), bits)
		if color != (0, 0, 0):
			# Fill image with color
			image[:] = color
		return image

	def update(self, dt):
		# Creating face cascade
		cascPath = "haarcascade_frontalface_default.xml"
		faceCascade = cv2.CascadeClassifier(cascPath)

        # display image from cam in opencv window
		ret, frame = self.capture.read()
	
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor = 1.1,
			minNeighbors = 5,
			minSize = (30, 30),
			flags = cv2.CASCADE_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		# Display the resulting frame
		#cv2.imshow("CV2 Image", frame)

        # convert it to texture
		buf1 = cv2.flip(frame, 0)
		buf = buf1.tostring()
		texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
		texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
		self.img1.texture = texture1


	def on_stop(self):
		self.capture.release()

class videoPanelWidget(Widget):
	def __init__(self, img, **kwargs):
		super(videoPanelWidget, self).__init__(**kwargs)
		self.add_widget(img)
		self.add_widget(Label(text="Welcome To Power Nap", pos=(550, 525), font_size='30sp', font_name='RobotoMono-Regular', size_hint=(.3, 1)))
		self.add_widget(Label(text="Created by Seth Brunwasser", pos=(560, 500), font_size='15sp', font_name='RobotoMono-Regular'))
		self.add_widget(Label(text="When faces are not detected in the video \nframe to the left, the display will be \nturned off. \n\nVarious settings can be adjusted below.", \
			pos=(560, 425), font_size='15sp', font_name='RobotoMono-Regular'))
		with self.canvas.before:
			Color(0, .5, .9, mode='rgb')
			self.rect = Rectangle(pos=(self.pos[0]*5/3, self.pos[1]*5/3), size=(self.size[0]*2, self.size[1]*5/3))

		self.bind(pos=self.update_rect)
		self.bind(size=self.update_rect)

	def update_rect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size


if __name__ == '__main__':
	PowerNapApp().run()