from ultralytics import YOLO
from PIL import Image

def load_model(cfg_model_path, device='cpu'):
    model = YOLO(cfg_model_path)
    model.to(device)
    return model

def infer_image(frame, model, confidence):
    results = model.predict(source=frame, show=False, conf=confidence, save=False) 
    
    for r in results:
        im_array = r.plot() 
        im = Image.fromarray(im_array[..., ::-1])  

    return im, results


