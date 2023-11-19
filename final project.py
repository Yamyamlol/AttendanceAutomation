import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
 
video_capture = cv2.VideoCapture(0)
Abhijeet = face_recognition.load_image_file("D:\Coding\mini project\images\Abhijeet.jpg")
AbhijeetEncoding = face_recognition.face_encodings(Abhijeet)[0]

Anmol = face_recognition.load_image_file("D:\Coding\mini project\images\Anmol.jpg")
AnmolEncoding= face_recognition.face_encodings(Anmol)[0]

Himanshu = face_recognition.load_image_file("D:\Coding\mini project\images\Himanshu.jpg")
HimanshuEncoding= face_recognition.face_encodings(Himanshu)[0]

Sanyam = face_recognition.load_image_file("D:\Coding\mini project\images\Sanyam.jpg")
SanyamEncoding= face_recognition.face_encodings(Sanyam)[0]

known_face_encoding = [AbhijeetEncoding, AnmolEncoding, HimanshuEncoding, SanyamEncoding]

known_faces_names = ["Abhijeet", "Anmol", "Himanshu", "Sanyam"]

students = known_faces_names.copy()
 
face_locations = []
face_encodings = []
face_names = []
s=True
 
 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
 
 
f = open(('D:/Coding/mini project/Attendance of ')+current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)
 
while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
 
            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_COMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 0.5
                fontColor              = (0,0,0)
                thickness              = 1
                lineType               = 2
 
                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
 
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
video_capture.release()
cv2.destroyAllWindows()
f.close()
