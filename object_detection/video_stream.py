import cv2
import pandas as pd
import streamlit as st
from object_detection.model import infer_image

class LiveIngredientDetector:
    def __init__(self, model, confidence=0.5):
        self.model = model
        self.confidence = confidence
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.detected_classes = set()

    def release_camera(self):
        if self.cap.isOpened():
            self.cap.release()

    def process_frame(self, frame):
        frame = cv2.resize(frame, (self.width, self.height))
        output_img, results = infer_image(frame, self.model, self.confidence)

        for detection in results:
            for detection_class in detection.boxes.cls.numpy().astype(int):
                self.detected_classes.add(self.model.names[int(detection_class)])

        return output_img

    def run_detection(self):
        output = st.empty()  
        stop = st.button("Stop Video Stream")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                st.write("Can't read frame, stream ended. Exiting")
                break

            processed_frame = self.process_frame(frame)

            output.image(processed_frame)

            if stop:
                break

        self.release_camera()

        if self.detected_classes:
            return list(self.detected_classes)
        else:
            st.warning("No ingredients detected.")
            return []