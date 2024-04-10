import tkinter as tk
from tkinter import simpledialog

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.geometry("300x200")

# Biến để lưu giữ thông tin từ Window B
info_from_b = ""

def open_window_b():
    # Tạo một cửa sổ phụ
    window_b = tk.Toplevel(root)
    window_b.geometry("300x200")

    # Hàm để gọi khi nút submit được nhấn
    def submit_and_open_c():
        global info_from_b
        # Lấy thông tin từ người dùng và lưu vào biến
        info_from_b = simpledialog.askstring("Input", "Enter your info:", parent=window_b)
        if info_from_b:
            # Đóng Window A và B, mở Window C
            window_b.destroy()
            root.withdraw()
            open_window_c()

    submit_btn = tk.Button(window_b, text="Submit", command=submit_and_open_c)
    submit_btn.pack()

def open_window_c():
    # Tạo một cửa sổ phụ
    window_c = tk.Toplevel()
    window_c.geometry("300x200")

    # Hiển thị thông tin từ Window B
    info_label = tk.Label(window_c, text=f"Info: {info_from_b}")
    info_label.pack()

    # Hàm để quay lại Window A
    def back_to_a():
        window_c.destroy()
        root.deiconify()

    back_btn = tk.Button(window_c, text="Back to A", command=back_to_a)
    back_btn.pack()

# Nút trên Window A để mở Window B
open_b_btn = tk.Button(root, text="Open Window B", command=open_window_b)
open_b_btn.pack()

root.mainloop()
