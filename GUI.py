import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from markattendance import mark_attendance_button_pressed
from faces import add_new_face

class SimpleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")

        # Load the background image using Pillow
        background_image_path = "D:/Coding/mini project/UI images/3395620.jpg"
        original_background_image = Image.open(background_image_path)

        # Resize the background image to match the screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        resized_background_image = original_background_image.resize((screen_width, screen_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(resized_background_image)

        # Create a label to display the resized background image
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Set the window size to a fixed value
        self.root.geometry("850x500")

        # Center the window on the screen
        self.center_window()

        # Add buttons with a hover effect
        mark_attendance_button = self.create_button("Mark Attendance", self.mark_attendance)
        mark_attendance_button.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)

        # Use a lambda function to delay the execution of add_face until the button is pressed
        add_face_button = self.create_button("Add Face to Database", lambda: self.add_face())
        add_face_button.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.1)

        train_database_button = self.create_button("Train Database", self.train_database)
        train_database_button.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.1)

        exit_button = self.create_button("Exit", self.root.destroy)
        exit_button.place(relx=0.1, rely=0.7, relwidth=0.3, relheight=0.1)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 850
        window_height = 500

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, font=("Arial", 12), bg="#8370ee", activebackground="#6f61a8")
        return button

    def mark_attendance(self):
        mark_attendance_button_pressed()

    def add_face(self):
        add_new_face()

    def train_database(self):
        print("Training Database")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUI(root)
    root.mainloop()
