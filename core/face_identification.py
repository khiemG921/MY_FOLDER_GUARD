import os
import cv2
import time
from deepface import DeepFace
from tkinter import messagebox

DIRECTIONS = ['DIRECT', 'UP', 'DOWN', 'LEFT', 'RIGHT']

def identify_face():
    # Mở camera để nhận diện khuôn mặt
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    time.sleep(1.5)
    cap.release()

    # Cắt ảnh thành 250x250 pixels
    frame = frame[145:145+250, 220:220+250, :]

    if not ret:
        messagebox.showerror("Face ID", "Failed to capture face from webcam.")
        return

    # Duyệt qua tất cả các tấm ảnh trong thư mục
    image_folder = './data/facial_images/'
    found_match = False
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        try:
            # So sánh khuôn mặt với ảnh trong thư mục
            result = DeepFace.verify(frame, image_path)

            if result['verified']:
                found_match = True
                break  # Dừng khi tìm thấy ảnh khớp
        except:
            continue

    cv2.destroyAllWindows()
    # Hiển thị thông báo kết quả nhận diện
    if found_match:
        messagebox.showinfo("Face ID", "Face recognized successfully.")
        return True
    else:
        messagebox.showwarning("Face ID", "No matching face found.")
        return False


def capture_face():
    # Thiết lập kết nối với webcam
    cap = cv2.VideoCapture(0)

    for direction in DIRECTIONS:
        messagebox.showinfo("Face ID", f"Please move your face {direction} and press 'C' to capture the image.")

        while cap.isOpened():
            ret, frame = cap.read()

            # Cắt ảnh thành 250x250 pixels
            frame = frame[145:145+250, 220:220+250, :]

            # Hiển thị hình ảnh trên màn hình
            cv2.imshow("Facial Identification", frame)

            # Nhấn phím 'c' để chụp ảnh
            if cv2.waitKey(1) & 0xFF == ord('c'):
                # Tạo đường dẫn ảnh duy nhất cho từng hình
                img_name = os.path.join("./data/facial_images/", f"{direction}.jpg")

                # Lưu ảnh vào file
                cv2.imwrite(img_name, frame)
                break


    # Giải phóng webcam
    cap.release()
    # Đóng cửa sổ hiển thị
    cv2.destroyAllWindows()

    messagebox.showinfo("Face ID", "Capture completed.")