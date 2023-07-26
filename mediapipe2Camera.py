# First, install OpenCV & Mediapipe:
# $ pip install opencv-python mediapipe

import cv2
import mediapipe as mp
import serial

arduinodata=serial.Serial("COM3",9600)
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

          
            while cap.isOpened() and cap1.isOpened():
              success, image = cap.read()
              s,imageback=cap1.read()
              if not success:
                print("Ignoring empty camera frame.")
                continue

              # IMAGE 1: FACE
              image1 = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
              image1.flags.writeable = False
              results = face_detection.process(image1)
              image1.flags.writeable = True
              image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
              image2 = cv2.cvtColor(cv2.flip(imageback, 1), cv2.COLOR_BGR2RGB)
              image2.flags.writeable = False
              resultsback = face_detection.process(image2)
              image2.flags.writeable = True
              image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)
              count=0
              if results.detections or resultsback.detections:
                if results.detections:
                  for detection in results.detections:
                    count=count+1
                    mp_drawing.draw_detection(image1, detection)
                if resultsback.detections:
                  for detection in resultsback.detections:
                    count=count-1
                    mp_drawing.draw_detection(image2, detection)
                
                print(count)
                if(count<0):
                  count=-count
                s=str(count)
                arduinodata.write(s.encode())
                count=0
              
              # HORIZONTAL & VERTICAL IMAGE CONCAT
              col1 = cv2.vconcat([image1])
       
              final = cv2.hconcat([col1])

              col2 = cv2.vconcat([image2])
       
              final2 = cv2.hconcat([col2])
              cv2.putText(final, 'Face Detection', (30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
              cv2.putText(final2, 'Face Detection2', (30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

              if (success):
                cv2.imshow('MediaPipe Demo', final)
              if (s):
                cv2.imshow('MediaPipe Face', final2)
              if cv2.waitKey(5) & 0xFF == 27:
                break

cap.release()
cap1.release()
cv2.destroyAllWindows()
