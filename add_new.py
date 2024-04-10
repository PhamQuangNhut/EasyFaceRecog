import cv2
from utils import save_db
from sqlalchemy.orm import sessionmaker
from DB import User, CheckRecord, engine
# Tạo session để thao tác với cơ sở dữ liệu
Session = sessionmaker(bind=engine)
session = Session()

name = input("Nhập tên của nhân viên: ")
number = input("Nhập số điện thoại: ")
new_user = User(full_name=name, number=number)
session.add(new_user)
session.commit()
# Establish a connection to the webcam
cap = cv2.VideoCapture(0)
while cap.isOpened(): 
    ret, frame = cap.read()
    
    # Collect anchors 
    if cv2.waitKey(1) & 0XFF == ord('p'):
         id = new_user.id
         full_name = new_user.full_name
         save_db(img = frame, id = id)
         print(f"Bạn đã lưu dữ liệu của Nhân viên {full_name} với Id {id} thành công")
         break
    # Show image back to screen
    cv2.imshow('Image', frame)
    
    # Breaking gracefully
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()