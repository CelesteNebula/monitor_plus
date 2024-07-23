from config.database import db

class TrafficData(db.Model):
    __tablename__ = 'traffic_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    carNum = db.Column(db.String(50), nullable=False)
    personNum = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)

    def __repr__(self):
        return f"<TrafficData(id={self.id}, carNum={self.carNum}, personNum={self.personNum}, time={self.time}, device_id={self.device_id})>"
