import cv2
import face_recognition
import sys

seth_image = face_recognition.load_image_file("training-data/Seth/Seth16.jpg")
seth_face_encoding = face_recognition.face_encodings(seth_image)[0]

sam_image = face_recognition.load_image_file("training-data/Sam/Sam10.jpg")
sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

seth_rogen_image = face_recognition.load_image_file("training-data/Seth Rogen/seth_rogen.jpg")
seth_rogen_face_encoding = face_recognition.face_encodings(seth_rogen_image)[0]

video_capture = cv2.VideoCapture(0)
counter = 0
face_names = []

while True:
	ret, image = video_capture.read()

	if not ret:
		break

	# Reduce face size to make calculations easier
	small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

	# Convert image from BGR color (OpenCV) to RGB color (face_recognition)
	small_frame = small_frame[:, :, ::-1]

	# To save CPU, only do calculations once every 3 frames
	if counter % 3 == 0:
		face_locations = face_recognition.face_locations(small_frame)
		face_encodings = face_recognition.face_encodings(small_frame, face_locations)

		for face_encoding in face_encodings:
			# See if there is a match for known faces
			match = face_recognition.compare_faces([seth_rogen_face_encoding, seth_face_encoding, sam_face_encoding], face_encoding, tolerance=0.5)
			name = "Unknown"

			if match[0]:
				name = "Seth Rogen"
			elif match[1]:
				name = "Seth"
			elif match[2]:
				name = "Sam"

			face_names.append(name)

	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Resize image to original size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below face
		cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 1)


	cv2.imshow('Video', image)
	counter += 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()