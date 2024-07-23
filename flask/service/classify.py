import cv2
import torch
from flask_socketio import SocketIO
from ultralytics import YOLO
from PIL import Image
from torchvision.transforms import functional as F
import base64

# 'bicycle', 'bus', 'car', 'motorbike', 'person'
# 用于存储统计数据
car_count = [0, 0, 0, 0]
person_count = [0, 0, 0, 0]
bicycle_count = [0, 0, 0, 0]
bus_count = [0, 0, 0, 0]
motorbike_count = [0, 0, 0, 0]
total_jam = [0, 0, 0, 0]
tmp_car_count = [0, 0, 0, 0]
tmp_person_count = [0, 0, 0, 0]


def preprocess_image(img):
    original_size = img.shape[:2]  # 保存原始图像尺寸 (height, width)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img = F.resize(img, [640, 640])
    img = F.to_tensor(img)
    img = img.unsqueeze(0)  # 添加batch维度
    return img, original_size


def process_video(video_path, namespace, socketio: SocketIO, model):
    cap = cv2.VideoCapture(video_path)
    index = int(namespace[-1]) - 1  # 从namespace获取视频索引
    frame_count = 0  # 帧计数器

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 24 == 0:  # 每24帧处理一次
            # 使用YOLOv8模型进行预测
            img, original_size = preprocess_image(frame)
            outputs = model(img)

            # 获取原始尺寸和缩放后的尺寸
            orig_h, orig_w = original_size
            resized_h, resized_w = 640, 640

            # 初始化计数器
            counts = {'person': 0, 'bicycle': 0, 'motorbike': 0, 'car': 0, 'bus': 0}

            # 处理识别结果并绘制在原帧上
            boxes = outputs[0].boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1 = int(x1 * orig_w / resized_w)
                y1 = int(y1 * orig_h / resized_h)
                x2 = int(x2 * orig_w / resized_w)
                y2 = int(y2 * orig_h / resized_h)

                conf = box.conf[0].item()
                cls = int(box.cls[0].item())

                label = model.names[cls]

                if label in counts:
                    counts[label] += 1
                    # 框选识别目标
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                2)

            tmp_car_count[index] = counts['car'] + counts['bicycle'] + counts['bus'] + counts['motorbike']
            tmp_person_count[index] = counts['person']
            car_count[index] += counts['car']
            person_count[index] += counts['person']
            bicycle_count[index] += counts['bicycle']
            bus_count[index] += counts['bus']
            motorbike_count[index] += counts['motorbike']
            total_jam[index] = counts['car'] + counts['person'] + counts['bicycle'] + counts['bus'] + counts[
                'motorbike']
            print(total_jam)

            # 将处理后的帧通过WebSocket发送给前端
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')

            # 调试信息，确保数据被发送
            print(f"Sending frame of length: {len(frame_data)} to namespace {namespace} with counts: {counts}")

            socketio.emit('video_frame', {'frame': frame_data, 'counts': counts, 'channel': namespace},
                          namespace=namespace)

    cap.release()
