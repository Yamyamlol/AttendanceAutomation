import face_recognition
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def load_images_from_folder(folder):
    images = []
    labels = []
    
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)
        
        if len(encoding) > 0:
            images.append(encoding[0])
            labels.append(filename.split('.')[0])  # Assuming file names are person names
    
    return images, labels

# Specify the path to your dataset folder
dataset_folder = "path/to/dataset"

# Load images and labels
images, labels = load_images_from_folder(dataset_folder)
import face_recognition
import os
from sklearn.neighbors import KNeighborsClassifier

def load_images_from_folder(folder):
    images = []
    labels = []
    
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)
        
        if len(encoding) > 0:
            person_name = filename.split('0')[0]  # Assuming '0' is the separator between name and index
            images.append(encoding[0])
            labels.append(person_name)
    
    return images, labels

# Specify the path to your dataset folder
dataset_folder = "path/to/dataset"

# Load images and labels
images, labels = load_images_from_folder(dataset_folder)

# Train a simple k-NN classifier
from sklearn.neighbors import KNeighborsClassifier

classifier = KNeighborsClassifier(n_neighbors=1)
classifier.fit(images, labels)

# Test the model
test_image_path = "path/to/test_image.jpg"
test_image = face_recognition.load_image_file(test_image_path)
test_encoding = face_recognition.face_encodings(test_image)

if len(test_encoding) > 0:
    predicted_label = classifier.predict([test_encoding[0]])[0]
    print(f"The predicted label for the test image is: {predicted_label}")
else:
    print("No face found in the test image.")

# Train a simple k-NN classifier
from sklearn.neighbors import KNeighborsClassifier

classifier = KNeighborsClassifier(n_neighbors=1)
classifier.fit(images, labels)

# Test the model
test_image_path = "path/to/test_image.jpg"
test_image = face_recognition.load_image_file(test_image_path)
test_encoding = face_recognition.face_encodings(test_image)

if len(test_encoding) > 0:
    predicted_label = classifier.predict([test_encoding[0]])[0]
    print(f"The predicted label for the test image is: {predicted_label}")
else:
    print("No face found in the test image.")
