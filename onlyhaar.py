import pygame
import cv2
import numpy as np
import serial

arduinodata=serial.Serial("COM3",9600)
video=cv2.VideoCapture(0)

faceDetect=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

pygame.init()

window=pygame.display.set_mode((1200,700))

pygame.display.set_caption("Face Detection App")

img=pygame.image.load("bg.png").convert()

start=True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start=False
            pygame.quit()
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(frame, 1.3, 5)
    fc=format(len(faces))
    arduinodata.write(fc.encode())
    
    for (x,y,w,h) in faces:
        x1,y1=x+w, y+h
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.line(frame, (x,y), (x+30, y),(0,0,255), 6) #Top Left
        cv2.line(frame, (x,y), (x, y+30),(0,0,255), 6)

        cv2.line(frame, (x1,y), (x1-30, y),(0,0,255), 6) #Top Right
        cv2.line(frame, (x1,y), (x1, y+30),(0,0,255), 6)

        cv2.line(frame, (x,y1), (x+30, y1),(0,0,255), 6) #Bottom Left
        cv2.line(frame, (x,y1), (x, y1-30),(0,0,255), 6)

        cv2.line(frame, (x1,y1), (x1-30, y1),(0,0,255), 6) #Bottom right
        cv2.line(frame, (x1,y1), (x1, y1-30),(0,0,255), 6)
    imgRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgRGB=np.rot90(imgRGB)
    imgRGB=pygame.surfarray.make_surface(imgRGB).convert()


    font=pygame.font.Font("BebasNeue-Regular.ttf", 50)
    text=font.render("Face Detected: {}".format(len(faces)), True, (255,255,255))
    
    
    window.blit(img, (0,0))
    window.blit(imgRGB, (280,95))
    pygame.draw.rect(window, (144,238,144), (280,50,640,70), border_top_left_radius=10, border_top_right_radius=10)
    pygame.draw.rect(window, (144,238,144), (280,550,640,70), border_bottom_left_radius=10, border_bottom_right_radius=10)
    window.blit(text, (320,50))
    pygame.display.update()
