import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

def save_to_csv(names, encodings, directory):
    today_date = datetime.now().strftime("%d-%m-%Y")
    csv_file_path = os.path.join(directory, f"Attendance_of_{today_date}.csv")

    existing_dates = set()

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size != 0:
            with open(csv_file_path, mode='r') as read_file:
                reader = csv.reader(read_file)
                next(reader, None)
                for row in reader:
                    existing_dates.add((row[0], row[2]))

        if not existing_dates:
            writer.writerow(["Name", "Time", "Date"])

        for name in names:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d-%m-%Y")

            if (name, current_date) not in existing_dates:
                writer.writerow([name, current_time, current_date])
                existing_dates.add((name, current_date))

    return csv_file_path

def read_encodings_from_data(file_path):
    names, encodings = [], []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])
            encoding_values = [float(value) for value in row[1:]]
            encoding = np.array(encoding_values)
            encodings.append(encoding)
    return names, encodings

def mark_attendance_with_face_recognition(data_file_path, destination_directory):
    known_faces_names, known_face_encodings = read_encodings_from_data(data_file_path)
    students = known_faces_names.copy()

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index] and face_distance[best_match_index] < 0.5:
                name = known_faces_names[best_match_index]

            face_names.append(name)

            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_COMPLEX
                bottom_left_corner_of_text = (10, 100)
                font_scale = 0.5
                font_color = (0, 0, 0)
                thickness = 1
                line_type = 2

                cv2.putText(frame, f"{name} Present",
                            bottom_left_corner_of_text,
                            font,
                            font_scale,
                            font_color,
                            thickness,
                            line_type)

                if name in students:
                    students.remove(name)
                    print(students)
                    now = datetime.now()
                    current_date = now.strftime("%Y-%m-%d")
                    print(f"Marking attendance for {name} at {current_date} {now.strftime('%H:%M:%S')}")
                    save_to_csv([name], [known_face_encodings[best_match_index]], 'D:\Coding\mini project\Attendance')

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
def mark_attendance_button_pressed():
    """
    Function to mark attendance using face recognition.
    """
    # Specify the path to the CSV file
    data_file_path = os.path.join('D:/Coding/mini project/database', "Data.txt")

    # Specify the path to the destination directory
    destination_directory = "D:/Coding/mini project/images"

    # Call the face recognition function
    mark_attendance_with_face_recognition(data_file_path, destination_directory)
    
if __name__ == "__main__":
    data_file_path = os.path.join('D:/Coding/mini project/database', "Data.txt")
    destination_directory = "D:/Coding/mini project/images"
    mark_attendance_with_face_recognition(data_file_path, destination_directory)
