from deepface.modules import detection, modeling, preprocessing, representation, verification
from deepface.models.FacialRecognition import FacialRecognition 
from deepface.models.Detector import Detector
from deepface.detectors.DetectorWrapper import build_model, rotate_facial_area
import cv2
import numpy as np 
from typing import Tuple, Union
from tensorflow.keras.preprocessing import image
import os 
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

def get_emb(img: Union[str, np.ndarray]) -> np.ndarray:
     image, _ = preprocessing.load_image(img)
     result = face_detector.detect_faces(image)
     result = result[0]
     aligned_img, angle = detection.align_face(
     img=image, left_eye=result.left_eye, right_eye=result.right_eye
     )
     rotated_x1, rotated_y1, rotated_x2, rotated_y2 = rotate_facial_area(
                    facial_area=(result.x, result.y, result.x + result.w, result.y + result.h),
                    angle=angle,
                    size=(image.shape[0], image.shape[1])
               )
     source_face = aligned_img[
                    int(rotated_y1) : int(rotated_y2),
                    int(rotated_x1) : int(rotated_x2)]
     source_img = source_face
     source_img = source_img.squeeze()
     source_img = source_img[:, :, ::-1]
     source_img = resize_image(source_img, (target_size[1], target_size[0]))
     source_img = preprocessing.normalize_input(img=source_img, normalization='base')
     source_emb = model.find_embeddings(source_img)
     source_emb = np.array(source_emb)
     return source_emb

def save_db(img: Union[str, np.ndarray], id: str, name: str) : 
     emb = get_emb(img)
     if os.path.exists('db.npy') : 
          db = np.load('db.npy', allow_pickle=True)
          new_e = np.array([id, emb])
          db = np.append(db, [new_e], axis=0)
          np.save('db.npy', db)
     else : 
          db = np.array([[id, emb], ])
          np.save('db.npy', db)
     # db = np.concatenate((db, emb))
     # np.save('db.npy', db)
     # loaded_array = np.load('db.npy', allow_pickle=True)
     print(f"Bạn đã lưu dữ liệu của Nhân viên {name} với Id {id} thành công")

def identify(
    image: Union[np.ndarray, list],
) -> str : 
     db = np.load('db.npy', allow_pickle=True)
     emb = get_emb(image)
     for id, emb_db in db :  
          distance = verification.find_distance(
                emb, emb_db, 'cosine'
          )
          print(distance)