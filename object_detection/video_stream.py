import cv2
import pandas as pd
import streamlit as st
from object_detection.model import infer_image

def live_input(model, confidence=0.5):
    """
    Capture live video from the camera, detect ingredients, and save them to a CSV.
    """
    cap = cv2.VideoCapture(0)  
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  

    # Create a placeholder for dynamic updates
    output = st.empty()  
    stop = st.button("Stop Video Stream")  
    detected_classes = set()  

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Can't read frame, stream ended. Exiting")
            break

        frame = cv2.resize(frame, (width, height)) # resize frame to current dimensions 
        output_img, result = infer_image(frame, model, confidence)

        # display the processed image in Streamlit (update dynamically)
        output.image(output_img)

        # loop over detected objects and store unique classes
        for detection in result:
            for detection_class in detection.boxes.cls.numpy().astype(int):
                detected_classes.add(model.names[int(detection_class)])
        
        if stop:
            cap.release()
            break

    cap.release() 
    
    if detected_classes:
        return list(detected_classes)
    else:
        st.warning("No ingredients detected.")
        return []
