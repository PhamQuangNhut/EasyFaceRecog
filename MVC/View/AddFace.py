import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
import os
import io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
import AIModule 
class AddFace:
    def __init__(self, root, employee):
        self.root = root
        self.employee = employee
        self.window = tk.Toplevel()
        self.window.title("PCheck")
        self.e_controller = self.root.e_controller
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.btn_submit = tk.Button(self.window, text="Submit", command=self.submit_data)
        self.btn_submit.pack(pady=10)

        self.btn_back = tk.Button(self.window, text="Quay lại", command=self.go_back)
        self.btn_back.pack(pady=10)

        self.lbl_message = tk.Label(self.window, text="", fg="red")
        self.lbl_message.pack()

        self.vid = cv2.VideoCapture(0)
        self.show_frame()

    def show_frame(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.show_frame)

    def close_camera(self):
        if self.vid.isOpened():
            self.vid.release()

    def submit_data(self):
        try:
            ret, frame = self.vid.read()
            if not ret:
                raise Exception("Không thể đọc frame từ camera")
            aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 = AIModule.face_detect(frame)
            face_img, face_emb = AIModule.get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)
            face_img = Image.fromarray(face_img)
            img_byte_arr = io.BytesIO()
            face_img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            success = self.e_controller.add_face(self.employee.id, img_byte_arr, face_emb)
            if success:
               messagebox.showinfo("Thông báo", f"Bạn đã lưu dữ liệu của Nhân viên {self.employee.full_name} với ID {self.employee.id} thành công")
            else : 
                messagebox.showinfo("Thông báo", f"Lưu dữ liệu của Nhân viên không thành công")
            self.go_back()  # Sử dụng hàm go_back để quay lại màn hình chính sau khi lưu dữ liệu thành công
        except Exception as e:
            self.lbl_message.config(text=f"Đã xảy ra lỗi: {e}")
    def __del__(self):
        if hasattr(self, 'vid') and self.vid.isOpened():
            self.vid.release()
        self.root.open_camera()
        self.root.show_main_window()
    def go_back(self):
        # Đóng cửa sổ hiện tại và quay lại màn hình chính
        self.close_camera()
        self.window.destroy()
        self.root.open_camera()
        self.root.show_main_window()