from deepface.modules import detection, modeling, preprocessing, representation, verification
from deepface.models.FacialRecognition import FacialRecognition 
from deepface.models.Detector import Detector
from deepface.detectors.DetectorWrapper import build_model, rotate_facial_area
import cv2
import numpy as np 
from typing import Tuple, Union
from tensorflow.keras.preprocessing import image
import os 
import config

model: FacialRecognition = modeling.build_model('ArcFace')
face_detector: Detector = build_model('ssd')
target_size = model.input_shape
def resize_image(img: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Resize an image to expected size of a ml model with adding black pixels.
    Args:
        img (np.ndarray): pre-loaded image as numpy array
        target_size (tuple): input shape of ml model
    Returns:
        img (np.ndarray): resized input image
    """
    factor_0 = target_size[0] / img.shape[0]
    factor_1 = target_size[1] / img.shape[1]
    factor = min(factor_0, factor_1)

    dsize = (
        int(img.shape[1] * factor),
        int(img.shape[0] * factor),
    )
    img = cv2.resize(img, dsize)

    diff_0 = target_size[0] - img.shape[0]
    diff_1 = target_size[1] - img.shape[1]

    # Put the base image in the middle of the padded image
    img = np.pad(
        img,
        (
            (diff_0 // 2, diff_0 - diff_0 // 2),
            (diff_1 // 2, diff_1 - diff_1 // 2),
            (0, 0),
        ),
        "constant",
    )

    # double check: if target image is not still the same size with target.
    if img.shape[0:2] != target_size:
        img = cv2.resize(img, target_size)

    # make it 4-dimensional how ML models expect
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    if img.max() > 1:
        img = (img.astype(np.float32) / 255.0).astype(np.float32)

    return img

def face_detect(image):
    try:
        image, _ = preprocessing.load_image(image)
        results = face_detector.detect_faces(image)
        
        if not results:
            raise ValueError("Không tìm thấy khuôn mặt trong khung hình")
        elif len(results) > 1: 
            raise ValueError("Phát hiện nhiều hơn một khuôn mặt trong khung hình")
        
        result = results[0]
        
        aligned_img, angle = detection.align_face(
            img=image, left_eye=result.left_eye, right_eye=result.right_eye
        )
        
        rotated_x1, rotated_y1, rotated_x2, rotated_y2 = rotate_facial_area(
            facial_area=(result.x, result.y, result.x + result.w, result.y + result.h),
            angle=angle,
            size=(image.shape[0], image.shape[1])
        )
        
        return aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2
    except FileNotFoundError:
        raise FileNotFoundError("Không thể tải ảnh")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

def get_emb(aligned_img: Union[str, np.ndarray],  rotated_x1: float, rotated_y1: float, rotated_x2: float, rotated_y2: float) -> np.ndarray:
    try:
        # Assuming preprocessing, detection, and other required modules are already imported and configured        
        source_face = aligned_img[
            int(rotated_y1): int(rotated_y2),
            int(rotated_x1): int(rotated_x2)
        ]

        source_img = source_face.squeeze()
        source_img = source_img[:, :, ::-1]  # Convert BGR to RGB if necessary

        # Assuming 'resize_image' and 'preprocessing.normalize_input' are defined elsewhere
        source_img = resize_image(source_img, (target_size[1], target_size[0]))
        source_img = preprocessing.normalize_input(img=source_img, normalization='base')

        source_emb = model.find_embeddings(source_img)
        source_emb = np.array(source_emb)

        return source_emb

    except Exception as e:
        # Handle exceptions such as no faces detected or other errors
        # Optionally, you can raise the error again if you want the exception to propagate
        # raise e


def save_db(img: Union[str, np.ndarray], id: int) : 
     aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2 =face_detect(img)
     _, emb = get_emb(aligned_img, rotated_x1, rotated_y1, rotated_x2, rotated_y2)

     if os.path.exists(config.VECTOR_DB_PATH) : 
          db = np.load(config.VECTOR_DB_PATH, allow_pickle=True)
          new_e = np.array([id,emb])
          db = np.append(db, [new_e], axis=0)
     else : 
          db = np.array([[id,emb], ])
     np.save(config.VECTOR_DB_PATH, db)
    

def identify(
    emb_vec: np.ndarray
) -> Tuple[str, str, float]:
    if not os.path.exists(config.VECTOR_DB_PATH):
        raise FileNotFoundError("Chưa có tệp cơ sở dữ liệu (db.npy)")

    result = []
    db = np.load(config.VECTOR_DB_PATH, allow_pickle=True)

    # Tính toán embedding của hình ảnh đầu vào

    # Tìm khoảng cách nhỏ nhất và lưu id của ảnh tương ứng
    min_distance = float('inf')
    min_id = None
    for id, emb_db in db:
        distance = verification.find_distance(emb_vec, emb_db, 'cosine')
        result.append((id, distance))
        
        if distance < min_distance:
            min_distance = distance
            min_id = id

    return min_id, min_distance
