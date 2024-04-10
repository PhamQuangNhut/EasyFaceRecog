import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import datetime
from utils import identify, face_detect, get_emb  # Đảm bảo bạn có file utils.py trong cùng thư mục
from sqlalchemy.orm import sessionmaker
from DB import User, CheckRecord, engine  # Đảm bảo bạn đã tạo DB.py và cấu hình cơ sở dữ liệu của mình
from add_face import NewFaceWindow
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

          # Button Mở cửa sổ mới và đóng cửa sổ hiện tại
          self.add_new = tk.Button(window, text="Thêm nhân viên", width=15, command=self.get_information)
          self.add_new.grid(row=2, column=1)

          # Hiển thị thông điệp
          self.lbl_message = tk.Label(window, text="", fg="red")
          self.lbl_message.grid(row=3, columnspan=3)

          self.update()

     def face_recognition(self, action_type):
          Session = sessionmaker(bind=engine)
          session = Session()

          ret, frame = self.vid.read()
          if ret:
               try:
                    aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 = face_detect(frame)
                    emb_vec = get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)
                    id, dist = identify(emb_vec)
                    print(dist)
                    if dist <= 0.6:
                         user = session.query(User).filter_by(id=id).first()
                         now = datetime.datetime.now()
                         check_record = CheckRecord(user_id=user.id, type=action_type, time=now)
                         session.add(check_record)
                         session.commit()

                         if action_type == "Check In":
                              if now.time() <= datetime.time(9, 0):  # Đi làm đúng giờ
                                   message = f"Chúc bạn {user.full_name} có một ngày làm việc vui vẻ. Cảm ơn bạn đã đi làm đúng giờ."
                              elif now.time() < datetime.time(8, 0):  # Đi sớm
                                   message = f"Bạn {user.full_name} thực sự là một nhân viên tốt. Sự đóng góp của bạn là sự thành công của công ty. Chúc bạn có một ngày làm việc vui vẻ."
                              else:  # Đi trễ
                                   message = f"Chúc bạn {user.full_name} có một ngày làm việc vui vẻ. Hy vọng ngày mai bạn sẽ đi làm đúng giờ."
                              self.lbl_message.config(text=message)

                         elif action_type == "Check Out":
                              checkin_time = session.query(CheckRecord).filter_by(user_id=user.id, type="Check In").order_by(CheckRecord.time.desc()).first().time
                              print(checkin_time)
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
     def get_information(self):
          app = AddEmployeeWindow(self)
          
     def open_camera(self):
          if not self.vid.isOpened():
               self.vid.open(self.video_source)
               print("Camera has been successfully opened.")
          else:
               print("Camera is already opened.")
     def close_camera(self):
          if self.vid.isOpened():
               self.vid.release()
          print("Camera has been successfully released.")
          
     def show_main_window(self):
          self.window.deiconify()
     def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class AddEmployeeWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent_window = parent.window
        self.window = tk.Toplevel(self.parent_window)
        self.window.title("Thêm thông tin nhân viên")

        # Label và Entry cho Tên nhân viên
        self.label_name = tk.Label(self.window, text="Tên nhân viên:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(self.window)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        # Label và Entry cho Số điện thoại
        self.label_phone = tk.Label(self.window, text="Số điện thoại:")
        self.label_phone.grid(row=1, column=0, padx=10, pady=5)
        self.entry_phone = tk.Entry(self.window)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=5)

        # Button Submit
        self.btn_submit = tk.Button(self.window, text="Xác nhận", command=self.submit_info)
        self.btn_submit.grid(row=2, columnspan=2, pady=10)

    def submit_info(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Xử lý logic khi nhấn nút Submit ở đây
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        if not name or not phone:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return  # Return to exit the function if there's an error
        try:
            existing_user = session.query(User).filter_by(number=phone).first()
            if existing_user:
                messagebox.showerror("Lỗi", "Số điện thoại đã tồn tại. Vui lòng nhập lại!")
            else:
                new_user = User(full_name=name, number=phone)
                session.add(new_user)
                session.commit()
                messagebox.showinfo("Thông báo", "Thêm hình ảnh gương mặt")
                # Create NewFaceWindow instance
                self.parent.close_camera()
                self.parent_window.withdraw()
                self.window.destroy()  # Destroy AddEmployeeWindow after submission
                new_face_window = NewFaceWindow(self.parent, name, new_user.id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"{str(e)}")
        finally:
            session.close()
        


# Tạo cửa sổ và bắt đầu ứng dụng
root = tk.Tk()
app = FaceRecognitionApp(root, "Điểm Danh")
root.mainloop()
