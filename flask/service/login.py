from model.admin import Admin
from config.database import db

def verify_admin_credentials(admin_id, admin_pw):
    admin = Admin.query.filter_by(admin_id=admin_id, admin_pw=admin_pw).first()

    if admin:
        return True, admin.admin_name
    return False, None
