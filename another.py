import face_recognition
import cv2
import numpy as np
import csv
import os
# import glob
from datetime import datetime

VideoCapture = cv2.VideoCapture(0)

Abhijeet = face_recognition.load_image_file("D:\Coding\mini project\images\Abhijeet.jpg")
AbhijeetEncoding = face_recognition.face_encoding(Abhijeet)[0]

Anmol = face_recognition.load_image_file("D:\Coding\mini project\images\Anmol.jpg")
AnmolEncoding= face_recognition.face_encoding(Anmol)[0]

Himanshu = face_recognition.load_image_file("D:\Coding\mini project\images\Himanshu.jpg")
HimanshuEncoding= face_recognition.face_encoding(Himanshu)[0]

Sanyam = face_recognition.load_image_file("D:\Coding\mini project\images\Sanyam.jpg")
SanyamEncoding= face_recognition.face_encoding(Sanyam)[0]

KnownFaceEncoding = [AbhijeetEncoding, AnmolEncoding, HimanshuEncoding, SanyamEncoding]

KnownFaceNames = ["Abhijeet", "Anmol", "Himanshu", "Sanyam"]

students = KnownFaceNames.copy()

FaceLocation = []
FaceEncodings = []
FaceNames = []
s = True

TimeNow = datetime.now()
TodayDate = TimeNow.striftime("%y-%m-%d")

f = open(TodayDate+".csv", 'w+', newline= '')
LineWriter = csv.writer(f)

while True:
    _,frame = VideoCapture.read()
    SmallFrame = cv2.resize(frame,(0,0),fx=0.25, fy=0.25)
    RGBSmallFrame = SmallFrame[:,:,::-1]
    if s:
        FaceLocation = face_recognition.FaceLocation = (RGBSmallFrame)
        FaceEncoding = face_recognition.FaceEncoding(RGBSmallFrame, FaceLocation)
        FaceNames = []
        for FaceEncoding in FaceEncodings:
            Matches = face_recognition.compare_faces(KnownFaceEncoding, FaceEncoding)
            name = ""
            FaceDistance = face_recognition.FaceDistance(KnownFaceEncoding, FaceEncoding)
            BestMatchIndex = np.argmin(FaceDistance)
            if Matches[BestMatchIndex]:
                name = KnownFaceNames[BestMatchIndex]
                
            FaceNames.append(name)
            if name in KnownFaceNames:
                if name in students:
                    students.remove(name)
                    print(students)
                    TimeOfAttendance = TimeNow.striftime("%H-%M-%S")
                    LineWriter.writerow([name, TimeOfAttendance])
        cv2.lnhow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
VideoCapture.release()
cv2.destroyAllWindows()
f.close()
