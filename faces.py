import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
from tkinter import filedialog
import shutil
import os

def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        print("Selected file:", file_path)

def move_to_directory(file_path):
    destination_directory = os.path.abspath("D:\Coding\mini project\images")  # Update with your actual directory
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    shutil.move(file_path, destination_directory)

class ArrayManager:
    def __init__(self):
        self.encodings = []
        self.names = []

    def add_face(self):
        # Increase the size of the array by 1 and initialize the new element to 0
        # temp = face_recognition.load_image_file()
        temp = 1
        # name = input('Enter your name: ')
        name = '0 '
        self.encodings.append(temp)
        self.names.append(name)
        print("Names:", self.names)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Add a New Face")

    # Create an instance of ArrayManager
    array_manager = ArrayManager()

    # Function to handle button click
    def on_button_click():
        array_manager.add_face()

    # Create a button widget
    add_face_button = tk.Button(root, text="Add Face", cursor="hand2", width=14, command = upload_file)
    add_face_button.grid(row=1, column=0)

    # Load and display the camera icon
    UploadIcon = Image.open(r'D:/Coding/mini project/images/upload-button.png')
    UploadIcon = UploadIcon.resize((100, 100), Image.ANTIALIAS)
    upload_icon = ImageTk.PhotoImage(UploadIcon)

    upload_button = tk.Button(root, image=upload_icon, cursor="hand2", command = upload_file)
    upload_button.image = upload_icon  
    # Keep a reference to prevent garbage collection
    upload_button.grid(row=0, column=0)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
