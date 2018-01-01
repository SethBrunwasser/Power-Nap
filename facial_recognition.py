import cv2
import os
import numpy as np
import time
'''
def detect_faces(video_capture, faceCascade):
	# Capture frame
	ret, frame = video_capture.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize = (30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

	return faces, ret, frame
'''
#function to detect face using OpenCV
def detect_faces(img):
	#convert the test image to gray scale as opencv face detector expects gray images
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	 
	#load OpenCV face detector, I am using LBP which is fast
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


def add_face(label, numOfImages):
	# Add new face to face recognition collection
	if not os.path.isdir("training-data/" + label):
		os.makedirs("training-data/" + label)
	cam = cv2.VideoCapture(0)
	for i in range(numOfImages):
		s, img = cam.read()
		cv2.imwrite("training-data/{}/{}{}.jpg".format(label, label, i), img)
		time.sleep(1)

def prepare_training_data(data_folder_path):
	dirs = os.listdir(data_folder_path)

	faces = []
	labels = []

	for dir_name in dirs:
		label = dir_name
		label_dir_path = data_folder_path + "/" + dir_name

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
						faces.append(face)
						if label == "Seth":
							labels.append(1)
						if label == "Sam":
							labels.append(2)

	cv2.destroyAllWindows()
	cv2.waitKey(1)
	cv2.destroyAllWindows()
	return faces, labels

def train_save():
	faces, labels = prepare_training_data("training-data")

	print("Total faces: ", len(faces))
	print("Total labels: ", len(labels))

	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	face_recognizer.train(faces, np.array(labels))

	face_recognizer.save('training-data/recognize_model.yml')

#add_face("Sam", 16)

subjects = {1: "Seth", 2: "Sam"}
train_save()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("training-data/recognize_model.yml")

def predict(test_img):
	img = test_img

	faces, rects = detect_faces(img)

	if faces is not None and rects is not None:
		
		for face, rect in zip(faces, rects):
			if face is not None and rect is not None:
				label = face_recognizer.predict(face)
				label_text = subjects[label[0]] + " - " + str(round(label[1], 1))

				(x, y, w, h) = rect
				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
				cv2.putText(img, label_text, (x, y - 15), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

	return img

video_capture = cv2.VideoCapture(0)
while True:

		ret, frame = video_capture.read()
		if frame is not None:
				recognized_face = predict(frame)
				# Draw a rectangle around the faces
				#or (x, y, w, h) in faces:
				#	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

				# Display the resulting frame
				cv2.imshow('Face Recognizer', recognized_face)

				if cv2.waitKey(1) & 0xFF == ord('q'):
					break