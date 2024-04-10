import cv2
import matplotlib.pyplot as plt
from utils import identify, face_detect, get_emb 
from sqlalchemy.orm import sessionmaker
import cv2
from DB import User, CheckRecord, engine

action = None
while True:
            action = input("Bạn muốn Check In hay Check Out? (I/O): ").strip().lower()
            if action == 'i':
                action_type = 'Check In'
                break
            elif action == 'o':
                action_type = 'Check Out'
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng nhập 'I' để Check In hoặc 'O' để Check Out.")

# Tạo session factory
Session = sessionmaker(bind=engine)

# Mở một session
session = Session()

# Establish a connection to the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened(): 
    ret, frame = cap.read()
    try:
        aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 = face_detect(frame)
    except Exception as e:
        print(f"Error during face detection: {e}")
        continue  # Skip the rest of this iteration and continue with the next iteration

    # Draw bounding box
    cv2.rectangle(frame, (rotated_x1, rotated_y1), (rotated_x2, rotated_y2), (0, 255, 0), 2)

    try:
        emb_vec = get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)
    except Exception as e:
        print(f"Error getting embedding: {e}")
        continue

    # Collect anchors 
    if cv2.waitKey(1) & 0xFF == ord('p'):
        try:
            id, dist = identify(emb_vec)
            if dist > 0.5: 
                print('Không có dữ liệu người này')
            else: 
                user = session.query(User).filter_by(id=id).first()
                print(f'Xin chào {user.full_name}, chúc bạn một ngày làm việc tốt lành')
                check_in = CheckRecord(user_id=user.id, type=action)
                session.add(check_in)
                session.commit()
            break
        except Exception as e:
            print(f"Error during identification: {e}")
            continue

    # Show image back to screen
    cv2.imshow('Image', frame)
    
    # Breaking gracefully
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When exiting the loop, release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
