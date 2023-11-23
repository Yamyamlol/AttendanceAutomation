import tkinter as tk
from tkinter import filedialog
import face_recognition
import shutil
import cv2
import os
import csv
import numpy as np

class ArrayManager:
    encodings = []
    names = []

def copy_to_directory(image, name, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for i in range(1, 11):
        destination_path = os.path.join(destination_directory, f"{name}{i}.jpg")
        cv2.imwrite(destination_path, image)
        print(f'The captured image has been saved to {destination_path}')
    return destination_path

def save_to_csv(names, encodings):
    csv_file_path = os.path.join('D:/Coding/mini project/database', "Data.txt")

    # Check if the file exists
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is newly created or empty
        if not file_exists or os.stat(csv_file_path).st_size == 0:
            writer.writerow(["Name", "Encoding"])

        # Write the data for each encoding
        for name, encoding in zip(names, encodings):
            # Normalize the encoding
            encoding = encoding / np.linalg.norm(encoding)

            # Convert encoding values to strings
            encoding_strings = [str(value) for value in encoding]
            writer.writerow([name] + encoding_strings)

    return csv_file_path

def capture_images(array_manager, name_entry):
    if len(array_manager.names) > 0:
        print("You have already entered a name.")
        return

    # Get the name from the entry widget
    name = name_entry.get()
    if not name:
        print("Please enter a name.")
        return

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Create a window to display the video feed
    cv2.namedWindow("Capture Face", cv2.WINDOW_NORMAL)

    # Counter for the number of frames with detected faces
    face_count = 0

    while face_count < 10:
        ret, frame = cap.read()

        # Encode the face
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            encoding = face_recognition.face_encodings(frame, face_locations)[0]

            # Store the name and encoding in the arrays
            array_manager.names.append(name)
            array_manager.encodings.append(encoding)
            print("Names:", array_manager.names)
            print("Encodings:", array_manager.encodings)

            # Save to destination directory
            destination_directory = os.path.abspath("D:/Coding/mini project/images")  # Update with your actual directory
            destination_path = copy_to_directory(frame, name, destination_directory)

            # Save to CSV file
            csv_file_path = save_to_csv(array_manager.names, array_manager.encodings)
            print(f'Data has been saved to {csv_file_path}')

            # Increment the face count
            face_count += 1
        else:
            print("No face found in the captured image.")

        # Display the video feed in the window
        cv2.imshow("Capture Face", frame)
        cv2.waitKey(1)  # Adjust the delay (milliseconds) based on your system

    # Release the webcam and destroy the window
    cap.release()
    cv2.destroyAllWindows()


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Add a New Face")

    # Create an instance of ArrayManager
    array_manager = ArrayManager()

    # Specify the directory where you want to save the CSV file
    destination_directory = os.path.abspath("D:/Coding/mini project/images")  # Update with your actual directory

    # Create an entry widget for the name
    name_entry = tk.Entry(root, width=28)
    name_entry.grid(row=0, column=0, pady=10)

    # Function to handle button click
    def on_button_click():
        capture_images(array_manager, name_entry)

    # Create a button widget
    add_face_button = tk.Button(root, text="Add Face", cursor="hand2", width=28, command=on_button_click)
    add_face_button.grid(row=1, column=0, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
