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
     def __init__(self, window, Session, face_embs, video_source):
          self.window = window
          self.window.title('PCheck')
          
          self.frame1 = tk.Frame(window)
          self.frame1.grid(row=0, column=0, padx=10, pady=10)
          
          self.video_source = video_source
          self.vid = cv2.VideoCapture(self.video_source, )
          
          self.e_controller = EmployeeController(Session, face_embs)
          self.record_controller = CheckRecordController(Session)
          self.image_width= int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
          self.image_height=int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
          self.canvas = tk.Canvas(self.frame1, width=self.image_width, height=self.image_height)
          self.canvas.grid(row=0, column=0, columnspan=3)
          

          # Button Check-in
          self.btn_checkin = tk.Button(self.frame1, text="Check-in", width=15, command=self.checkin, bg='green')
          self.btn_checkin.grid(row=1, column=0 , sticky='w')

          # Hiển thị giờ hiện tại
          self.lbl_time = tk.Label(self.frame1, text="")
          self.lbl_time.grid(row=1, column=1, sticky='n')
          self.update_clock()

          # Button Check-out
          self.btn_checkout = tk.Button(self.frame1, text="Check-out", width=15, command=self.checkout, bg='blue', )
          self.btn_checkout.grid(row=1, column=2, sticky='e')

          # Button Mở cửa sổ mới và đóng cửa sổ hiện tại
          self.add_new = tk.Button(self.frame1, text="Thêm nhân viên", width=15, command=self.add_employee)
          self.add_new.grid(row=2, column=1)
          
          
          # Hiển thị thông điệp
          
          
          self.frame2 = tk.Frame(window, padx=10, pady=10)
          self.frame2.grid(row=0, column=1, sticky='nw')
          
          self.record_face_label = tk.Label(self.frame2, bg="lightgrey")  # Label để hiển thị hình ảnh
          self.record_face_label.grid(row=0, column=0, sticky='nw')  # Đặt ở bên phải
          self.record_information = tk.Label(self.frame2, pady=10) 
          self.record_information.grid(row=1, column=0, sticky='w')
          
          
          
          self.frame3 = tk.Frame(window, padx=10, pady=10)
          self.frame3.grid(row=0, column=2, sticky='nw')
          self.user_face_label = tk.Label(self.frame3, bg="lightgrey") # Label để hiển thị hình ảnh
          self.user_face_label.grid(row=0, column=0, sticky='nw')  # Đặt ở bên phải

          
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
                         
                         face_img = Image.fromarray(face_img)
                         face_img = face_img.resize(AIModule.model_size)
                         
                         img_byte_arr = io.BytesIO()
                         photo_image = ImageTk.PhotoImage(face_img)
                         
                         # Configure the label with the new image
                         self.record_face_label.configure(image=photo_image)
                         self.record_face_label.image = photo_image  # Keeping a reference to avoid garbage collection
                         img_byte_arr = img_byte_arr.getvalue()
                         user, dist = self.e_controller.get_employee_by_face_emb(face_emb)
                         print(dist)
                         
                         if dist <= 0.6:
                              face_img = Image.open(io.BytesIO(user.face_img))
                              face_img = face_img.resize(AIModule.model_size)
                              
                              photo_image = ImageTk.PhotoImage(face_img)
                              self.user_face_label.configure(image=photo_image)
                              self.user_face_label.image = photo_image
                              now = datetime.datetime.now()
                              check_record = self.record_controller.add_check_record(user_id=user.id, type=action_type, time=now, face_img=img_byte_arr)
                              if action_type == "Check In":
                                   self.record_information.config(
                                   text=f"Tên Nhân Viên: {user.full_name} \n"
                                           f"Số điện thoại: {user.number} \n"
                                           f"Thời gian checkin: {now.hour}:{now.minute} \n"
                                           ,anchor='w'
                                           ,justify='left'
                                           ,fg="black"
                                   )

                              elif action_type == "Check Out":
                                   checkin_time = self.record_controller.get_lastest_checkin_records_by_user_id(user.id)
                                   time_diff = now - checkin_time
                                   hours = time_diff.seconds // 3600
                                   minutes = (time_diff.seconds // 60) % 60
                                   self.record_information.config(
                                   text=  f"Tên Nhân Viên: {user.full_name}\n"
                                             f"Số điện thoại: {user.number}\n"
                                             f"Thời gian checkout: {now.hour}:{now.minute}\n"
                                             f"Thời gian checkint gần nhất: {checkin_time.hour}:{checkin_time.minute}\n"
                                             f"Đã làm việc được: {hours}:{minutes}\n"
                                             ,anchor='w'
                                             ,justify='left'
                                             ,fg="black"
                                   )
                         else:
                              
                              self.record_information.config(text = "Không có dữ liệu người này", fg="red")
                              self.user_face_label.configure(image=None)
               except Exception as e:
                    self.record_information.config(text=f"{e}", fg="red")
                    self.user_face_label.configure(image=None)
                    self.user_face_label.image = None
                    self.record_face_label.configure(image=None)
                    self.record_face_label.image = None
                    
          else:
               self.record_information.config(text='Không thể đọc dữ liệu từ camera', fg="red")
               self.user_face_label.configure(image=None)
               self.user_face_label.image = None
               self.record_face_label.configure(image=None)
               self.record_face_label.image = None

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
                    bbox_color = (0, 255, 0)  
                     
                    # face_img, face_emb = AIModule.get_emb(face['aligned_img'], face['rotated_x1'], face['rotated_y1'], face['rotated_x2'], face['rotated_y2'])
                    # user, dist = self.e_controller.get_employee_by_face_emb(face_emb)

                    # if dist > 0.6:
                    #     # Set bounding box color to red and do not display the name
                    #     bbox_color = (255, 0, 0)  # Red color
                    # else:
                    #     # Set bounding box color to green and display the name
                    #     bbox_color = (0, 255, 0)  # Green color
                    # #     name_and_dist = f"{user.fsull_name} ({dist:.2f})"
                    #     name = f"{user.full_name}"
                    #     font = ImageFont.truetype("arial.ttf", 16)
                    #     text_position = (face['rotated_x1'], face['rotated_y1'] - 20)
                    #     draw.text(text_position, name, font=font, fill=(255, 255, 255))

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