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
    results = model.predict(source=frame, show=False, conf=confidence, save=False) # it contains like class ID, class names, coordinates of bounding boxes
    
    for r in results:
        im_array = r.plot()  # plot the image with bounding boxes
        im = Image.fromarray(im_array[..., ::-1])  # convert BGR to RGB for display
        
    return im, results


