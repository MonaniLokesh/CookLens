from ultralytics import YOLO

def train_model():
    model_path = 'yolov8s.pt'
    data_path = 'datasets/data.yaml'

    model = YOLO(model_path)

    model.train(
        data=data_path,  
        epochs=100,      
        imgsz=640,     
        plots=True,      
    )

if __name__ == "__main__":
    train_model()
