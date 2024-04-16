import tkinter as tk
from tkinter import messagebox
from View.AddFace import AddFace
class AddEmployee:
    def __init__(self, root):
        self.root = root
        self.parent_window = root.window
        self.window = tk.Toplevel(self.parent_window)
        self.window.title("Thêm thông tin nhân viên")

        # Label và Entry cho Tên nhân viên
        self.label_name = tk.Label(self.window, text="Tên nhân viên:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(self.window)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        # Label và Entry cho Số điện thoại
        self.label_number = tk.Label(self.window, text="Số điện thoại:")
        self.label_number.grid(row=1, column=0, padx=10, pady=5)
        self.entry_number = tk.Entry(self.window)
        self.entry_number.grid(row=1, column=1, padx=10, pady=5)

        # Button Submit
        self.btn_submit = tk.Button(self.window, text="Xác nhận", command=self.submit_info)
        self.btn_submit.grid(row=2, columnspan=2, pady=10)
        self.e_controller = self.root.e_controller

    def submit_info(self):
        # Xử lý logic khi nhấn nút Submit ở đây
        full_name = self.entry_name.get()
        number = self.entry_number.get()
        if not full_name or not number:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return  # Return to exit the function if there's an error
        try:
            existing_user = self.e_controller.get_employee_by_number(number = number)
            if existing_user:
                messagebox.showerror("Lỗi", "Số điện thoại đã tồn tại. Vui lòng nhập lại!")
            else:
                new_employee = self.e_controller.add_employee(full_name=full_name, number=number, have_face = False)
                messagebox.showinfo("Thông báo", "Thêm hình ảnh gương mặt")
                # Create NewFaceWindow instance
                self.root.close_camera()
                self.parent_window.withdraw()
                self.window.destroy()  # Destroy AddEmployeeWindow after submission
                add_face_window = AddFace(self.root, new_employee)
        except Exception as e:
            messagebox.showerror("Lỗi", f"{str(e)}")