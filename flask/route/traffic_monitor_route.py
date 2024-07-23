from flask import Blueprint
from flask_socketio import SocketIO
import threading
import cv2
from service.classify import process_video
from ultralytics import YOLO

traffic_monitor = Blueprint('traffic_monitor', __name__)
socketio = SocketIO()

# 预先加载模型
model = YOLO('D://PycharmProjects/teamProject3/best.pt')

def video_thread(video_path, namespace):
    process_video(video_path, namespace, socketio, model)

@traffic_monitor.route('/start')
def start_monitoring():
    print("已经开始视频")
    video_paths = ['D://PycharmProjects/teamProject3/0.mp4', 'D://PycharmProjects/teamProject3/1.mp4', 'D://PycharmProjects/teamProject3/2.mp4', 'D://PycharmProjects/teamProject3/3.mp4']
    namespaces = ['/video1', '/video2', '/video3', '/video4']

    for video_path, namespace in zip(video_paths, namespaces):
        thread = threading.Thread(target=video_thread, args=(video_path, namespace))
        thread.start()

    return "Video monitoring started"

@socketio.on('connect', namespace='/video1')
def handle_video1_connect():
    print("Client connected to /video1")

@socketio.on('connect', namespace='/video2')
def handle_video2_connect():
    print("Client connected to /video2")

@socketio.on('connect', namespace='/video3')
def handle_video3_connect():
    print("Client connected to /video3")

@socketio.on('connect', namespace='/video4')
def handle_video4_connect():
    print("Client connected to /video4")