from config.database import db

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_pw = db.Column(db.String(50), nullable=False)
    admin_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Admin(admin_id={self.admin_id}, admin_name={self.admin_name})>"
