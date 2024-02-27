import os
import cv2
import face_recognition

class Camera:
    def __init__(self):
        # Initialize the camera object
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        
        # Set the video codec to MJPG
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # Load known persons from images in the "sources" folder
        self.persons = self.load_persons("sources")

    def load_persons(self, photos_folder):
        # Initialize a list to store information about known persons
        persons = []

        # Loop through files in the photos folder
        for filename in os.listdir(photos_folder):
            # Check if the file is an image
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Extract person's name from the filename
                person_name = os.path.splitext(filename)[0]
                
                # Load the image using face_recognition library
                person_image_path = os.path.join(photos_folder, filename)
                person_image = face_recognition.load_image_file(person_image_path)
                
                # Encode the face of the person in the image
                person_face_encoding = face_recognition.face_encodings(person_image)[0]
                
                # Append person's name and face encoding to the list of persons
                persons.append({'name': person_name, 'encoding': person_face_encoding})

        return persons

    def recognize_person(self, face_encoding):
        # Compare face encoding with known persons' encodings
        for person in self.persons:
            matches = face_recognition.compare_faces([person['encoding']], face_encoding)
            if any(matches):
                return person['name']

        return "Unknown"

    def start_camera(self):
        # Create a window to display the camera feed
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera', 600, 450)

        while True:
            # Capture frame-by-frame from the camera
            ret, frame = self.cap.read()

            # Find face locations in the frame
            face_locations = face_recognition.face_locations(frame)
            for (top, right, bottom, left) in face_locations:
                # Encode the face found in the frame
                face_encoding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]
                
                # Recognize the person based on the face encoding
                person_name = self.recognize_person(face_encoding)

                # Draw a rectangle around the detected face
                color = (0, 255, 0) if person_name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Display the name of the recognized person
                label = person_name
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Display the frame with face detections
            cv2.imshow('Camera', frame)

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()
