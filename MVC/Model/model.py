from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pytz
import config 
import numpy as np
import os
# Định nghĩa múi giờ GMT+7
timezone = pytz.timezone('Etc/GMT-7')
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    number = Column(String, unique=True, nullable=False)
    have_face = Column(Boolean, nullable=True)
    face_img = Column(LargeBinary, nullable=True)  
    
class CheckRecord(Base):
    __tablename__ = 'check_records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('employees.id'))
    time = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0))
    type = Column(Integer, nullable=False)  # 'Check In' hoặc 'Check Out'
    face_img = Column(LargeBinary, nullable=True)  
    user = relationship("Employee")
    

def get_session(db_file):
    engine = create_engine(f'sqlite:///{db_file}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
if os.path.exists(config.VECTOR_DB_PATH) : 
    face_embs = np.load(config.VECTOR_DB_PATH, allow_pickle=True)
else : 
    face_embs = None