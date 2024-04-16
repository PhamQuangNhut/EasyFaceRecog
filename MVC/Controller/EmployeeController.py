import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
from Model.model import Employee
import numpy as np
from deepface.modules import verification
import config
class EmployeeController:
    def __init__(self, session, face_embs):
        self.session = session
        self.face_embs = face_embs
    def add_employee(self, full_name, number, have_face=False, face_img=None, face_emb=None):
        new_employee = Employee(full_name=full_name, number=number, have_face=have_face, face_img=face_img)
        
        # if os.path.exists(config.VECTOR_DB_PATH) : 
        #        new_e = np.array([new_employee.id,face_emb])
        #        self.face_embs = np.append(self.face_embs, [new_e], axis = 0)
        # else : 
        #        self.face_embs = np.array([[new_employee.id,face_emb], ])
        # np.save(config.VECTOR_DB_PATH, self.face_embs)
        self.session.add(new_employee)
        self.session.commit()
        return new_employee
    
    
    def add_face(self, id, face_img, face_emb):
        employee = self.session.query(Employee).filter_by(id=id).first()
        if employee:
            employee.have_face = True
            employee.face_img = face_img
            if os.path.exists(config.VECTOR_DB_PATH) : 
                new_e = np.array([employee.id,face_emb])
                self.face_embs = np.append(self.face_embs, [new_e], axis = 0)
            else : 
                self.face_embs = np.array([[employee.id,face_emb], ])
            self.session.commit()
            np.save(config.VECTOR_DB_PATH, self.face_embs)
            return True
        return False
    def update_employee(self, id, full_name=None, number=None, have_face=None, face_img=None):
        employee = self.session.query(Employee).filter_by(id=id).first()
        if employee:
            if full_name:
                employee.full_name = full_name
            if number:
                employee.number = number
            if have_face is not None:
                employee.have_face = have_face
            if face_img:
                employee.face_img = face_img
            self.session.commit()
            return True
        return False
    def update_face(self, id, face_img, face_emb):
        employee = self.session.query(Employee).filter_by(id=id).first()
        if employee and employee.have_face:
            employee.face_img = face_img
            for idx, emb_db in enumerate(self.face_embs):
                if emb_db[0] == id:
                    self.face_embs[idx][1] = face_emb
                    break
            self.session.commit()
            return True
        return False
    def delete_employee(self, id):
        employee = self.session.query(Employee).filter_by(id=id).first()
        if employee:
            self.session.delete(employee)
            idx = np.where(self.face_embs[:, 0] == id)[0]
            if idx.size > 0:
               db = np.delete(db, idx, axis=0)
            self.session.commit()
            np.save(config.VECTOR_DB_PATH, self.face_embs)
            return True
        return False
    def delete_face(self, id): 
          employee = self.session.query(Employee).filter_by(id=id).first()
          if employee and employee.have_face:
              employee.have_face = False
              employee.face_img = None
              for idx, emb_db in enumerate(self.face_embs):
                    if emb_db[0] == id:
                         self.face_embs[idx] = [id, np.zeros_like(emb_db[1])] 
                         np.save(config.VECTOR_DB_PATH, self.face_embs)
              self.session.commit()
              return True
          return False
    def get_employee_by_number(self, number):
        return self.session.query(Employee).filter_by(number=number).all()

    def get_employee_by_full_name(self, full_name):
        return self.session.query(Employee).filter(Employee.full_name.like(f'%{full_name}%')).all()

    def get_employee_by_have_face(self, have_face):
        return self.session.query(Employee).filter_by(have_face=have_face).all()

    def get_employee_by_id(self, id):
        return self.session.query(Employee).filter_by(id=id).first()
    
    def get_employee_by_face_emb(self, face_emb:np.ndarray):
        if os.path.exists(config.VECTOR_DB_PATH) : 
            min_distance = float('inf')
            min_id = None
            for id, face_db in self.face_embs:

                distance = verification.find_distance(face_emb, face_db, 'cosine')
                if distance < min_distance:
                    min_distance = distance
                    min_id = id
            return self.session.query(Employee).filter_by(id=min_id).first(), min_distance
        else : 
            raise ValueError("Chưa có cơ sở dữ liệu khuôn mặt")
