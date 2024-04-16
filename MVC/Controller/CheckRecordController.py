from Model.model import CheckRecord

class CheckRecordController:
    def __init__(self, session):
        self.session = session

    def add_check_record(self, user_id, type, time, face_img=None):
        new_check_record = CheckRecord(user_id=user_id, type=type, time=time, face_img=face_img)
        self.session.add(new_check_record)
        self.session.commit()

    def update_check_record(self, check_record_id, type):
        check_record = self.session.query(CheckRecord).filter_by(id=check_record_id).first()
        if check_record:
            check_record.type = type
            self.session.commit()
            return True
        return False

    def delete_check_record(self, check_record_id):
        check_record = self.session.query(CheckRecord).filter_by(id=check_record_id).first()
        if check_record:
            self.session.delete(check_record)
            self.session.commit()
            return True
        return False

    def get_check_records_by_user_id(self, user_id):
        return self.session.query(CheckRecord).filter_by(user_id=user_id).all()
    
    def get_lastest_checkin_records_by_user_id(self, user_id):
        return self.session.query(CheckRecord).filter_by(user_id=user_id, type="Check In").order_by(CheckRecord.time.desc()).first().time