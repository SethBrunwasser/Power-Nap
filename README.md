# PrivaCV

PrivaCV (Privacy-V) is an application that performs facial recognition to determine which faces in the webcam are authorized to see the information on the computer display. If an unauthorized or unknown face is detected, the screen display will turn off.

Model initially trains on ~15 images of an individuals face. I then used semi-supervised learning to dynamically update the model with live face data as it's running. The goal is to reinforce the face data of the primary user of the computer without needing substantial training data.

Future Developments:
- Create RESTful API
