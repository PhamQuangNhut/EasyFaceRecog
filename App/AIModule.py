from deepface.modules import detection, modeling, preprocessing
from deepface.models.FacialRecognition import FacialRecognition 
from deepface.models.Detector import Detector
from deepface.detectors.DetectorWrapper import build_model, rotate_facial_area
import numpy as np 
from typing import Tuple, Union
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2
import tensorflow as tf
recognition_model: FacialRecognition = modeling.build_model('GhostFaceNet')
detection_model: Detector = build_model('yolov8')
target_size = recognition_model.input_shape
liveness_model = tf.keras.models.load_model('./AI_Checkpoint/liveness.model')
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

def liveness_detect(face_img: np.ndarray) -> bool :
    face_img = resize_image(face_img, (32, 32))
    # face_img = np.expand_dims(face_img, axis = 0)
    livenesss = liveness_model.predict(face_img)
    
    return livenesss[0].argmax()
    
def face_detect(image):
    try:
        image, _ = preprocessing.load_image(image)
        results = detection_model.detect_faces(image)
        
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

def faces_detect(image):
    try:
        image, _ = preprocessing.load_image(image)
        results = detection_model.detect_faces(image)
        
        if not results:
            raise ValueError("Không tìm thấy khuôn mặt trong khung hình")
        # elif len(results) > 1: 
        #     raise ValueError("Phát hiện nhiều hơn một khuôn mặt trong khung hình")
        list = []
        # result = results[0]
        for result in results : 
            aligned_img, angle = detection.align_face(
                img=image, left_eye=result.left_eye, right_eye=result.right_eye
            )
            
            rotated_x1, rotated_y1, rotated_x2, rotated_y2 = rotate_facial_area(
                facial_area=(result.x, result.y, result.x + result.w, result.y + result.h),
                angle=angle,
                size=(image.shape[0], image.shape[1])
            )
            list.append({'aligned_img': aligned_img, 'rotated_x1': rotated_x1, 'rotated_y1': rotated_y1, 'rotated_x2': rotated_x2, 'rotated_y2': rotated_y2})
        
        return list
    except FileNotFoundError:
        raise FileNotFoundError("Không thể tải ảnh")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

def get_emb(aligned_img: Union[str, np.ndarray],  rotated_x1: float, rotated_y1: float, rotated_x2: float, rotated_y2: float) -> np.ndarray:
    try:
        # Assuming preprocessing, detection, and other required modules are already imported and configured        
        face_img = aligned_img[
            int(rotated_y1): int(rotated_y2),
            int(rotated_x1): int(rotated_x2)
        ]

        face_img = face_img.squeeze()
        face_img = face_img[:, :, ::-1]  # Convert BGR to RGB if necessary

        # Assuming 'resize_image' and 'preprocessing.normalize_input' are defined elsewhere
        face_emb = resize_image(face_img, (target_size[1], target_size[0]))
        face_emb = preprocessing.normalize_input(img=face_emb, normalization='base')

        face_emb = recognition_model.find_embeddings(face_emb)
        face_emb = np.array(face_emb)

        return face_img, face_emb

    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}. Please try again with a different image.")
   
   
