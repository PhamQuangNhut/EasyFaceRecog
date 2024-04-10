import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import datetime
from utils import identify, face_detect, get_emb  # Đảm bảo bạn có file utils.py trong cùng thư mục
from sqlalchemy.orm import sessionmaker
from DB import User, CheckRecord, engine  # Đảm bảo bạn đã tạo DB.py và cấu hình cơ sở dữ liệu của mình

class FaceRecognitionApp:
     def __init__(self, window, window_title):
          self.window = window
          self.window.title(window_title)
          self.video_source = 0

          # Màn hình hiển thị video
          self.vid = cv2.VideoCapture(self.video_source, )
          self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
          self.canvas.grid(row=0, columnspan=3)

          # Button Check-in
          self.btn_checkin = tk.Button(window, text="Check-in", width=15, command=self.checkin, bg='green')
          self.btn_checkin.grid(row=1, column=0)

          # Hiển thị giờ hiện tại
          self.lbl_time = tk.Label(window, text="")
          self.lbl_time.grid(row=1, column=1)
          self.update_clock()

          # Button Check-out
          self.btn_checkout = tk.Button(window, text="Check-out", width=15, command=self.checkout, bg='blue')
          self.btn_checkout.grid(row=1, column=2)

          # Hiển thị thông điệp
          self.lbl_message = tk.Label(window, text="", fg="red")
          self.lbl_message.grid(row=2, columnspan=3)

          self.update()

     def face_recognition(self, action_type):
     # Tạo session factory và mở một session
          Session = sessionmaker(bind=engine)
          session = Session()

          ret, frame = self.vid.read()
          if ret:
               try:
                    aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 = face_detect(frame)
                    emb_vec = get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)
                    id, dist = identify(emb_vec)
                    if dist <= 0.5:  # Điều chỉnh ngưỡng phù hợp với yêu cầu của bạn
                         user = session.query(User).filter_by(id=id).first()
                         check_record = CheckRecord(user_id=user.id, type=action_type)
                         session.add(check_record)
                         session.commit()
                         if action_type == "Check In" : 
                              self.lbl_message.config(text=f"Xin chào {user.full_name}, chúc bạn một ngày làm việc tốt lành")
                         elif action_type == "Check Out" : 
                              self.lbl_message.config(text=f"Tạm biệt {user.full_name}, ngày mai lại cố gắng làm việc nhé")
                    else:
                         self.lbl_message.config(text='Không có dữ liệu người này')
               except Exception as e:
                    self.lbl_message.config(text=f"Lỗi: {e}")
          else:
               self.lbl_message.config(text='Không thể đọc dữ liệu từ camera')

          # Đóng session
          session.close()

     def checkin(self):
        # Xử lý check-in bằng cách sử dụng nhận diện khuôn mặt
        self.face_recognition('Check In')

     def checkout(self):
        # Xử lý check-out bằng cách sử dụng nhận diện khuôn mặt
        self.face_recognition('Check Out')

     def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl_time.config(text=now)
        self.window.after(1000, self.update_clock)

     def update(self):
        # Lấy frame từ video source
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(10, self.update)

     def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Tạo cửa sổ và bắt đầu ứng dụng
root = tk.Tk()
app = FaceRecognitionApp(root, "Ứng Dụng Điểm Danh")
root.mainloop()
