import os
from ultralytics import YOLO

def train_model():
    best_model_path = 'runs/detect/train6/weights/best.pt'  # 之前训练最好模型的路径

    if os.path.exists(best_model_path):
        # 加载之前训练的最好模型
        model = YOLO(best_model_path)
        print(f"Loaded existing best model from {best_model_path}")
    else:
        # 加载默认的预训练模型，从头训练
        model = YOLO('yolov10x.pt')
        print("No existing best model found. Starting training from scratch.")

    # 训练模型
    model.train(
        data='data.yaml', 
        epochs=50, 
        batch=16, 
        imgsz=640, 
        lr0=0.00001,
        lrf=0.01,  # 调整学习率衰减
        optimizer='SGD', 
        momentum=0.937,  # 优化器动量
        weight_decay=0.0005,  # 权重衰减
        warmup_epochs=5.0,  # 增加热身轮数
        augment=True  # 开启数据增强
    )

    # 评估模型
    metrics = model.val()
    print(metrics)

    # 导出模型为.pth格式
    # model.save('trained_model.pth')  # 导出训练好的模型

if __name__ == '__main__':
    train_model()
