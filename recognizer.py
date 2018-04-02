import cv2
import os
import numpy as np
import time

class Recognizer(object):
	"""docstring for Recognizer"""
	def __init__(self, load=False):
		super(Recognizer, self).__init__()

		self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		if not load:
			self.face_recognizer.read("LBPH_recognize_model.yml")

		self.training_data_path = "training-data/"

	def train_save(self, db):
		faces, labels = prepare_training_data("training-data", db)

		print("Total faces: ", len(faces))
		print("Total labels: ", len(labels))

		self.face_recognizer.set("threshold", 100)
		self.face_recognizer.train(faces, np.array(labels))
		self.face_recognizer.save('LBPH_recognize_model.yml')
	
	#function to detect faces using OpenCV
	def detect_faces(self, img):
		#convert the test image to gray scale as opencv face detector expects gray images
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		
		#load OpenCV face detector, I am using LBPH which is fast
		#there is also a more accurate but slow: Haar classifier
		cascPath = "haarcascade_frontalface_alt2.xml"
		
		face_cascade = cv2.CascadeClassifier(cascPath)

		#let's detect multiscale images(some images may be closer to camera than others)
		#result is a list of faces
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
		 
		#if no faces are detected then return original img
		if len(faces) == 0:
			return None, None
		 
		#under the assumption that there will be only one face for training images,
		#extract the face area
		elif len(faces) == 1:
			(x, y, w, h) = faces[0]
			return [gray[y:y+w, x:x+h]], faces
		else:
			#return only the face part of the image
			return [gray[y:y+w, x:x+h] for x, y, w, h in faces], faces


	def predict(self, subjects, test_img):
		img = test_img

		faces, rects = self.detect_faces(img)

		if faces is not None and rects is not None:
			temp_labels = []
			temp_faces = []
			for face, rect in zip(faces, rects):
				if face is not None and rect is not None:
					resized_webcam_face = cv2.resize(face, (100, 100), interpolation=cv2.INTER_CUBIC)
					label = self.face_recognizer.predict(resized_webcam_face)
					temp_labels.append(label[0])
					temp_faces.append(face)

					label_text = subjects[label[0]] + " - " + str(round(label[1], 1))

					(x, y, w, h) = rect
					cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
					cv2.putText(img, label_text, (x, y - 15), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
			return img, temp_labels, temp_faces
		return img, None, None

	def update(self, faces, labels):
		self.face_recognizer.update(faces, np.array(labels))
		self.face_recognizer.save("LBPH_recognize_model.yml")

	def prepare_training_data(self, db):
		dirs = os.listdir(self.training_data_path)

		faces = []
		labels = []

		HEIGHT, WIDTH = cv2.imread(self.training_data_path + "/Seth/Seth0.jpg").shape[:2]
		print("Height: {} Width: {}".format(HEIGHT, WIDTH))

		for dir_name in dirs:
			label = dir_name
			label_dir_path = self.training_data_path + "/" + dir_name

			image_names = os.listdir(label_dir_path)
			for image_name in image_names:
				image_path = label_dir_path + "/" + image_name
				image = cv2.imread(image_path)
				cv2.imshow("Training on image..", image)
				cv2.waitKey(100)
				detected_faces, rect = detect_faces(image)
				if detected_faces is not None:
					for face in detected_faces:
						if face is not None:

							resized_face = cv2.resize(face, (100, 100), interpolation=cv2.INTER_CUBIC)
							faces.append(resized_face)
							user_id = db.query_id(label)
							print(user_id)
							labels.append(user_id)

		cv2.destroyAllWindows()
		cv2.waitKey(1)
		cv2.destroyAllWindows()
		return faces, labels

	def add_face(self, label, numOfImages):
		# Add new face to face recognition collection
		if not os.path.isdir("training-data/" + label):
			os.makedirs("training-data/" + label)
		cam = cv2.VideoCapture(0)
		for i in range(numOfImages):
			s, img = cam.read()
			cv2.imwrite("training-data/{}/{}{}.jpg".format(label, label, i), img)
			time.sleep(1)
