from flask import Flask, render_template
from flask_socketio import SocketIO
from route.traffic_monitor_route import traffic_monitor, socketio
from route.admin_route import admin_route
from route.data_route import data_route
from config.database import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xingyu2002@127.0.0.1:3306/traffic_monitor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(traffic_monitor)
app.register_blueprint(admin_route)
app.register_blueprint(data_route)

socketio.init_app(app, cors_allowed_origins='*')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
