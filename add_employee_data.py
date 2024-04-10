import tkinter as tk
from tkinter import ttk
from DB import User, engine  # Import model User và engine từ DB.py

class AddEmployeeData:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Tạo các label và entry để nhập dữ liệu của nhân viên mới
        self.lbl_name = tk.Label(window, text="Tên nhân viên:")
        self.lbl_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = tk.Entry(window)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.lbl_number = tk.Label(window, text="Số điện thoại:")
        self.lbl_number.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_number = tk.Entry(window)
        self.entry_number.grid(row=1, column=1, padx=10, pady=5)

        # Tạo button để thêm nhân viên mới
        self.btn_add = tk.Button(window, text="Thêm", width=10, command=self.add_employee)
        self.btn_add.grid(row=2, columnspan=2, pady=10)

    def add_employee(self):
        # Lấy dữ liệu từ các entry
        name = self.entry_name.get()
        number = self.entry_number.get()

        # Kiểm tra xem dữ liệu có tồn tại không trước khi thêm vào cơ sở dữ liệu
        if name and number:
            # Tạo một đối tượng User mới và thêm vào cơ sở dữ liệu
            new_user = User(full_name=name, number=number)
            with engine.connect() as con:
                con.execute(User.__table__.insert(), {"full_name": name, "number": number})
            
            # Thông báo thành công
            tk.messagebox.showinfo("Thông báo", "Thêm nhân viên mới thành công!")
        else:
            # Thông báo lỗi nếu dữ liệu không hợp lệ
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin của nhân viên!")

# Tạo cửa sổ và bắt đầu ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = AddEmployeeData(root, "Thêm Nhân Viên Mới")
    root.mainloop()
