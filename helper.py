import cv2
import face_recognition
import numpy as np
import ollama

import main

with open('prompt.md') as file:
    prompt = file.read()

with open('request.md') as file:
    prompt_req = file.read()


def findEncoding(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    return encode


my_encoded = findEncoding(cv2.imread("./Images/h.jpeg"))
sample = findEncoding(cv2.imread("./Images/mom.jpeg"))
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    # img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces([my_encoded, sample], encodeFace)
        faceDis = face_recognition.face_distance([my_encoded, sample], encodeFace)
        matchIndex = np.argmin(faceDis)
        if faceDis.item(matchIndex) < 0.5:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, 'name', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            # print("found")
            g = ollama.generate("gemma:2b", prompt)
            main.talk(g['response'])
            while True:
                command = main.take_command()
                g = ollama.generate("gemma:2b", prompt_req.replace("<input>", command))
                main.talk(g['response'])
    # cv2.imshow('Webcam', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        cv2.destroyAllWindows()
        break
