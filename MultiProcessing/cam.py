import cv2

# Khởi tạo biến đếm
counter = 0

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Kiểm tra nếu webcam được mở thành công
if not cap.isOpened():
    print("Không thể mở webcam")
else:
    # Vòng lặp liên tục để lấy và hiển thị khung hình từ webcam
    while True:
        # Lấy khung hình từ webcam
        ret, frame = cap.read()
        
        # Kiểm tra nếu việc lấy khung hình thất bại
        if not ret:
            print("Không thể lấy khung hình")
            break
        
        # Hiển thị khung hình trong cửa sổ có tên 'Webcam'
        cv2.imshow('Webcam', frame)
        
        # Đọc phím bấm
        key = cv2.waitKey(1) & 0xFF
        
        # Kiểm tra nếu phím 'a' được bấm
        if key == ord('a'):
            # Tăng biến đếm mỗi khi nhấn 'a'
            counter += 1
            print(f"Số lần nhấn phím 'a': {counter}")
        
        # Thoát khỏi vòng lặp khi người dùng nhấn phím 'q'
        elif key == ord('q'):
            break

    # Đóng webcam và đóng cửa sổ hiển thị
    cap.release()
    cv2.destroyAllWindows()