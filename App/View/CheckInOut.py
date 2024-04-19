import cv2 
import tkinter as tk
import datetime
from PIL import Image, ImageTk, ImageFont, ImageDraw
from Controller.EmployeeController import EmployeeController
from Controller.CheckRecordController import CheckRecordController
from View.AddEmployee import AddEmployee
from View.Employees import Employees

import sys
import os
import io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
import AIModule 
class CheckInOut:
     def __init__(self, window, Session, face_embs):
          self.window = window
          self.window.title('PCheck')
          self.video_source = 0
          self.vid = cv2.VideoCapture(self.video_source, )
          
          self.e_controller = EmployeeController(Session, face_embs)
          self.record_controller = CheckRecordController(Session)
          
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

          # Button Mở cửa sổ mới và đóng cửa sổ hiện tại
          self.add_new = tk.Button(window, text="Thêm nhân viên", width=15, command=self.add_employee)
          self.add_new.grid(row=2, column=1)
          
          # self.btn_employees = tk.Button(window, text="Quản lý nhân viên", width=15, command=self.employees)
          # self.btn_employees.grid(row=4, column=1)
          # Hiển thị thông điệp
          self.lbl_message = tk.Label(window, text="", fg="red")
          self.lbl_message.grid(row=3, columnspan=3)
          
          self.Session = Session
          self.show_frame()

     def face_recognition(self, action_type):
          ret, frame = self.vid.read()
          if ret:
               try:
                    detected_faces = AIModule.faces_detect(frame)  # Assuming this returns a list of face data
                    for face in detected_faces:
                         aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 = (
                              face['aligned_img'], face['rotated_x1'], face['rotated_y1'], face['rotated_x2'], face['rotated_y2']
                         )
                         face_img, face_emb = AIModule.get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)
                         is_live = AIModule.liveness_detect(face_img)
                         if is_live: 
                              face_img = Image.fromarray(face_img)
                              img_byte_arr = io.BytesIO()
                              face_img.save(img_byte_arr, format='PNG')
                              img_byte_arr = img_byte_arr.getvalue()
                              user, dist = self.e_controller.get_employee_by_face_emb(face_emb)
                              print(dist)

                              if dist <= 0.6:
                                   now = datetime.datetime.now()
                                   check_record = self.record_controller.add_check_record(user_id=user.id, type=action_type, time=now, face_img=img_byte_arr)

                                   if action_type == "Check In":
                                        if now.time() <= datetime.time(9, 0):  # On time
                                             message = f"Chúc bạn {user.full_name} có một ngày làm việc vui vẻ. Cảm ơn bạn đã đi làm đúng giờ."
                                        elif now.time() < datetime.time(8, 0):  # Early
                                             message = f"Bạn {user.full_name} thực sự là một nhân viên tốt. Sự đóng góp của bạn là sự thành công của công ty. Chúc bạn có một ngày làm việc vui vẻ."
                                        else:  # Late
                                             message = f"Chúc bạn {user.full_name} có một ngày làm việc vui vẻ. Hy vọng ngày mai bạn sẽ đi làm đúng giờ."
                                        self.lbl_message.config(text=message)

                                   elif action_type == "Check Out":
                                        checkin_time = self.record_controller.get_lastest_checkin_records_by_user_id(user.id)
                                        worked_hours = (now - checkin_time).total_seconds() / 3600
                                        if worked_hours < 8:
                                             message = f"Cảm ơn bạn {user.full_name} đã có một ngày làm việc tốt. Hình như hôm nay bạn làm việc chưa đủ 8 giờ. Ngày mai bạn bù nhé."
                                        else:
                                             message = f"Cảm ơn bạn {user.full_name} đã có một ngày làm việc tốt. Bạn là một nhân viên tốt, sự thành công của công ty là nhờ sự đóng góp của bạn rất nhiều."
                                        self.lbl_message.config(text=message)
                              else:
                                   self.lbl_message.config(text='Không có dữ liệu người này')
               except Exception as e:
                    self.lbl_message.config(text=f"Lỗi: {e}")
          else:
               self.lbl_message.config(text='Không thể đọc dữ liệu từ camera')

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

     def show_frame(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            pil_img = Image.fromarray(frame)  # Convert to PIL Image
            draw = ImageDraw.Draw(pil_img)  # Create a drawing context

            try:
                detected_faces = AIModule.faces_detect(frame)
                for face in detected_faces:
                    face_img, face_emb = AIModule.get_emb(face['aligned_img'], face['rotated_x1'], face['rotated_y1'], face['rotated_x2'], face['rotated_y2'])
                    is_live = AIModule.liveness_detect(face_img)
                    if is_live :
                         user, dist = self.e_controller.get_employee_by_face_emb(face_emb)

                         if dist > 0.6:
                         # Set bounding box color to red and do not display the name
                              bbox_color = (255, 0, 0)  # Red color
                         else:
                         # Set bounding box color to green and display the name
                              bbox_color = (0, 255, 0)  # Green color
                              #     name_and_dist = f"{user.fsull_name} ({dist:.2f})"
                              name = f"{user.full_name}"
                              font = ImageFont.truetype("arial.ttf", 16)
                              text_position = (face['rotated_x1'], face['rotated_y1'] - 20)
                              draw.text(text_position, name, font=font, fill=(255, 255, 255))

                              # Draw bounding box with specified color
                              draw.rectangle([face['rotated_x1'], face['rotated_y1'], face['rotated_x2'], face['rotated_y2']], outline=bbox_color, width=2)
            except Exception as e:
                print("Error in face detection:", e)

            # Convert back to ImageTk and update canvas
            self.photo = ImageTk.PhotoImage(image=pil_img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next frame update
        self.window.after(10, self.show_frame)
     def add_employee(self):
          app = AddEmployee(self)
     def employees(self):
          # Mở cửa sổ quản lý nhân viên
          window = tk.Toplevel(self.window)
          window.title("Pchat")
          app = Employees(window, self.e_controller)  # Khởi tạo giao diện quản lý nhân viên tại đây
     def open_camera(self):
          if not self.vid.isOpened():
               self.vid.open(self.video_source)
     def close_camera(self):
          if self.vid.isOpened():
               self.vid.release()
          
     def show_main_window(self):
          self.window.deiconify()
     def __del__(self):
        if hasattr(self, 'vid') and self.vid.isOpened():
            self.vid.release()