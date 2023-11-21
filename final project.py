import face_recognition
import cv2
import numpy as np
import csv
import os
import shutil
from datetime import datetime

def read_encodings_from_csv():
    names = []
    encodings = []
    with open('D:\Coding\mini project\database', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            names.append(row[0])
            encoding = np.array(row[1:], dtype=float)
            encodings.append(encoding)
    return names, encodings

def copy_to_directory(file_path, name, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    destination_path = os.path.join(destination_directory, f"{name}.jpg")
    shutil.copy(file_path, destination_path)
    return destination_path

def save_to_csv(names, encodings, directory):
    csv_file_path = os.path.join(directory, "Data.txt")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name"] + [f"Encoding_{i+1}" for i in range(len(encodings[0]))])
        for name, encoding in zip(names, encodings):
            writer.writerow([name] + list(encoding))
    return csv_file_path

# Specify the path to the CSV file
csv_file_path = os.path.join('D:\Coding\mini project\database', "Data.txt")

# Read names and encodings from the CSV file
known_faces_names, known_face_encoding = read_encodings_from_csv()

# Specify the path to the destination directory
destination_directory = "D:/Coding/mini project/images"  # Update with your actual directory

students = known_faces_names.copy()
 
face_locations = []
face_encodings = []
face_names = []

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
f = open(os.path.join(destination_directory, f"Attendance of {current_date}.csv"), 'w+', newline='')
lnwriter = csv.writer(f)
lnwriter.writerow(["S. NO", "NAME", "TIME", "DATE"])
 
video_capture = cv2.VideoCapture(0)

while True:
    i = 1
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
        name = ""
        face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
        best_match_index = np.argmin(face_distance)
        if matches[best_match_index]:
            name = known_faces_names[best_match_index]

        face_names.append(name)

        if name in known_faces_names:
            font = cv2.FONT_HERSHEY_COMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 0.5
            fontColor = (0, 0, 0)
            thickness = 1
            lineType = 2

            cv2.putText(frame, name + ' Present',
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
                lnwriter.writerow([i, name, current_time, current_date])
                i = i + 1

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
