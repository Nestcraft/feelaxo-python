from . import db


class Staff(db.Model):
    __tablename__ = 'attendance_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, nullable=False)
    business_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text)
    staff_phone = db.Column(db.Text)
    encodings = db.Column(db.Text)

    def __repr__(self):
        return f'<Staff id:{self.id}, staff_id:{self.staff_id}, business_id:{self.business_id}>'