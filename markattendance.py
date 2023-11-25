import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

def save_to_csv(names, encodings, directory):
    TodayDate = datetime.now().strftime("%d-%m-%Y")
    csv_file_path = os.path.join(directory, "Attendance of"+TodayDate+".csv")

    # Load existing attendance data to check if already marked for today
    existing_dates = set()
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is newly created or empty
        if not file_exists or os.stat(csv_file_path).st_size == 0:
            writer.writerow(["Name", "Time", "Date"])

        # Load existing dates if the file is not empty
        elif file_exists:
            with open(csv_file_path, mode='r') as read_file:
                reader = csv.reader(read_file)
                next(reader, None)  # Skip the header row if it exists
                for row in reader:
                    name = row[0]
                    date = row[2]  # Assuming date is at index 2
                    existing_dates.add((name, date))

        for name in names:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d-%m-%Y")  # Change format to match CSV

            # Check if attendance for today is already marked for this person
            if (name, current_date) not in existing_dates:
                writer.writerow([name, current_time, current_date])
                existing_dates.add((name, current_date))

    return csv_file_path


def read_encodings_from_csv(file_path):
    names = []
    encodings = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            names.append(row[0])
            encoding_values = [float(value) for value in row[1:]]
            encoding = np.array(encoding_values)
            encodings.append(encoding)
    return names, encodings

# ... (other functions)

if __name__ == "__main__":
    # Specify the path to the CSV file
    csv_file_path = os.path.join('D:/Coding/mini project/database', "Data.txt")

    # Read names and encodings from the CSV file
    known_faces_names, known_face_encodings = read_encodings_from_csv(csv_file_path)

    # Specify the path to the destination directory
    destination_directory = "D:/Coding/mini project/images"  # Update with your actual directory

    students = known_faces_names.copy()

    face_locations = []
    face_encodings = []
    face_names = []

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    # Use mode 'a' to append to the existing CSV file
    f = open(os.path.join(destination_directory, f"Attendance.csv"), 'a', newline='')

    video_capture = cv2.VideoCapture(0)

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

            if matches[best_match_index] and face_distance[best_match_index] < 0.5:  # Adjust the threshold as needed
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

                    # Debug: Print information about the attendance
                    print(f"Marking attendance for {name} at {current_date} {now.strftime('%H:%M:%S')}")

                    save_to_csv([name], [known_face_encodings[best_match_index]], 'D:\Coding\mini project\Attendance')

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()
