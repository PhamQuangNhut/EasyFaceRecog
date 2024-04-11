from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pytz
import config 
# Định nghĩa múi giờ GMT+7
timezone = pytz.timezone('Etc/GMT-7')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    number = Column(String, unique=True, nullable=False)

class CheckRecord(Base):
    __tablename__ = 'check_records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    time = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0))
    type = Column(String, nullable=False)  # 'Check In' hoặc 'Check Out'
    user = relationship("User")
    
engine = create_engine(f'sqlite:///{config.SQLITE_DB_PATH}')

# Tạo tất cả các bảng
Base.metadata.create_all(engine)