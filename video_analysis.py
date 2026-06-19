import cv2
import numpy as np

def analyze_eye_contact(video_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(video_path)

    total_frames, eye_contact_frames = 0, 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            eye_contact_frames += 1

    cap.release()
    if total_frames == 0:
        return 0
    return (eye_contact_frames / total_frames) * 100
