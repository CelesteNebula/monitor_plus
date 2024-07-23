from flask import Blueprint, request, jsonify
from service.login import verify_admin_credentials

admin_route = Blueprint('admin_route', __name__)

@admin_route.route('/login', methods=['POST'])
def login():
    data = request.json
    admin_id = data.get('admin_id')
    admin_pw = data.get('admin_pw')

    is_valid, admin_name = verify_admin_credentials(admin_id, admin_pw)
    if is_valid:
        return jsonify({'success': True, 'admin_name': admin_name}), 200
    return jsonify({'success': False, 'message': 'Invalid ID or password'}), 401
