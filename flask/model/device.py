from config.database import db

class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)

    def __repr__(self):
        return f"<Device(device_id={self.device_id}, admin_id={self.admin_id})>"
