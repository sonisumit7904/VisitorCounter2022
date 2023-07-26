# First, install OpenCV & Mediapipe:
# $ pip install opencv-python mediapipe

import cv2
import mediapipe as mp
import serial

arduinodata=serial.Serial("COM3",9600)
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(1)

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

          
            while cap.isOpened():
              success, image = cap.read()
              if not success:
                print("Ignoring empty camera frame.")
                continue

              # IMAGE 1: FACE
              image1 = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
              image1.flags.writeable = False
              results = face_detection.process(image1)
              image1.flags.writeable = True
              image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
              count=0
              if results.detections:
                for detection in results.detections:
                  count=count+1
                  mp_drawing.draw_detection(image1, detection)
                print(count)
                s=str(count)
                arduinodata.write(s.encode())
                count=0
              
              # HORIZONTAL & VERTICAL IMAGE CONCAT
              col1 = cv2.vconcat([image1])
       
              final = cv2.hconcat([col1])
              cv2.putText(final, 'Face Detection', (30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                
              cv2.imshow('MediaPipe Demo', final)
              if cv2.waitKey(5) & 0xFF == 27:
                break

cap.release()
