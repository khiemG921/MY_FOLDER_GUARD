import os
import cv2
import time
from deepface import DeepFace
from tkinter import messagebox

DIRECTIONS = ['DIRECT', 'UP', 'DOWN', 'LEFT', 'RIGHT']

def identify_face():
    # Open the webcam to capture the face
    cap = cv2.VideoCapture(0)

    # Read a frame from the camera
    ret, frame = cap.read()
    time.sleep(1.5)  # Add a delay to allow the camera to adjust
    cap.release()  # Release the webcam

    # Crop the image to 250x250 pixels for facial recognition
    frame = frame[145:145+250, 220:220+250, :]

    if not ret:
        # Display an error message if capturing fails
        messagebox.showerror("Face ID", "Failed to capture face from webcam.")
        return

    # Check all images in the folder for face matching
    image_folder = './data/facial_images/'
    found_match = False
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        try:
            # Compare the captured face with the current image in the folder
            result = DeepFace.verify(frame, image_path)

            if result['verified']:
                found_match = True
                break  # Stop searching when a matching face is found
        except:
            continue

    cv2.destroyAllWindows()
    
    # Display the result of face identification
    if found_match:
        messagebox.showinfo("Face ID", "Face recognized successfully.")
        return True
    else:
        messagebox.showwarning("Face ID", "No matching face found.")
        return False


def capture_face():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Capture images based on movement directions
    for direction in DIRECTIONS:
        messagebox.showinfo("Face ID", f"Please move your face {direction} and press 'C' to capture the image.")

        while cap.isOpened():
            ret, frame = cap.read()

            # Crop the image to 250x250 pixels
            frame = frame[145:145+250, 220:220+250, :]

            # Display the image in a window
            cv2.imshow("Facial Identification", frame)

            # Capture the image when 'c' is pressed
            if cv2.waitKey(1) & 0xFF == ord('c'):
                # Create a unique file path for the captured image
                img_name = os.path.join("./data/facial_images/", f"{direction}.jpg")

                # Save the image to the file
                cv2.imwrite(img_name, frame)
                break

    # Release the webcam
    cap.release()
    # Close the display window
    cv2.destroyAllWindows()

    # Notify the user that the capture process is complete
    messagebox.showinfo("Face ID", "Capture completed.")