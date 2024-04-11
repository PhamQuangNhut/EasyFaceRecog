import tkinter as tk
import cv2
from PIL import Image, ImageTk
from utils import save_db
from tkinter import messagebox

class NewFaceWindow:
    def __init__(self, parent, name, id):
        self.parent = parent
        self.name = name
        self.id = id
        self.window = tk.Toplevel()
        self.window.title("Thêm Nhân Viên")

        # Màn hình hiển thị hình ảnh từ camera
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        # Button Submit
        self.btn_submit = tk.Button(self.window, text="Submit", command=self.submit_data)
        self.btn_submit.pack(pady=10)

        # Button Quay lại
        self.btn_back = tk.Button(self.window, text="Quay lại", command=self.go_back)
        self.btn_back.pack(pady=10)

        # Label để hiển thị thông báo
        self.lbl_message = tk.Label(self.window, text="", fg="red")
        self.lbl_message.pack()

        # Khởi tạo camera
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
        print("Camera has been successfully released.")

    def submit_data(self):
        try:
            ret, frame = self.vid.read()
            if not ret:
                raise Exception("Không thể đọc frame từ camera")

            save_db(img=frame, id=self.id)
            messagebox.showinfo("Thông báo", f"Bạn đã lưu dữ liệu của Nhân viên {self.name} với ID {self.id} thành công")
            self.go_back()  # Sử dụng hàm go_back để quay lại màn hình chính sau khi lưu dữ liệu thành công
        except Exception as e:
            self.lbl_message.config(text=f"Đã xảy ra lỗi: {e}")

    def go_back(self):
        # Đóng cửa sổ hiện tại và quay lại màn hình chính
        self.close_camera()
        self.window.destroy()
        self.parent.open_camera()
        self.parent.show_main_window()
