import tkinter as tk
from tkinter import filedialog
import face_recognition
import shutil
import os
import csv

class ArrayManager:
    encodings = []
    names = []

def copy_to_directory(file_path, name):
    destination_directory = os.path.abspath("D:/Coding/mini project/images")  # Update with your actual directory
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    destination_path = os.path.join(destination_directory, f"{name}.jpg")
    shutil.copy(file_path, destination_path)
    return destination_path

def save_to_csv(names, encodings):
    csv_file_path = os.path.join('D:\Coding\mini project\database', "Data.txt")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Encoding"])
        for name, encoding in zip(names, encodings):
            writer.writerow([name, encoding])
    return csv_file_path

def upload_file(array_manager, name_entry, directory):
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        print("Selected file:", file_path)

        # Get the name from the entry widget
        name = name_entry.get()
        if not name:
            print("Please enter a name.")
            return

        # Encode the face
        face_image = face_recognition.load_image_file(file_path)
        encoding = face_recognition.face_encodings(face_image)[0]

        # Store the name and encoding in the arrays
        array_manager.names.append(name)
        array_manager.encodings.append(encoding)
        print("Names:", array_manager.names)
        print("Encodings:", array_manager.encodings)

        # Copy the file to the destination directory
        destination_path = copy_to_directory(file_path, name)
        print(f'The selected image has been copied to {destination_path}')

        # Save to CSV file
        csv_file_path = save_to_csv(array_manager.names, array_manager.encodings)
        print(f'Data has been saved to {csv_file_path}')

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
        upload_file(array_manager, name_entry, destination_directory)

    # Create a button widget
    add_face_button = tk.Button(root, text="Add Face", cursor="hand2", width=28, command=on_button_click)
    add_face_button.grid(row=1, column=0, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
