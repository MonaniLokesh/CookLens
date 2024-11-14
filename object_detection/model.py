from ultralytics import YOLO
from PIL import Image

def load_model(cfg_model_path, device='cpu'):
    """
    Load the YOLO model with the given configuration file path.
    """
    model = YOLO(cfg_model_path)
    model.to(device)
    return model

def infer_image(frame, model, confidence):
    """
    Run inference on a single frame and return the image with detected bounding boxes.
    """
    results = model.predict(source=frame, show=False, conf=confidence, save=False) 
    
    for r in results:
        im_array = r.plot() 
        im = Image.fromarray(im_array[..., ::-1])  
        
    return im, results


