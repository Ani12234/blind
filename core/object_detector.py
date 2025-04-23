import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Dict
import math

class ObjectDetector:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Initialize the object detector with YOLOv8 model.
        
        Args:
            model_path: Path to the YOLOv8 model weights
        """
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        
    def detect_objects(self, image: np.ndarray) -> List[Dict]:
        """
        Detect objects in the given image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of dictionaries containing detected objects with their properties
        """
        results = self.model(image)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Calculate object center and approximate distance
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                
                # Simple distance estimation based on object size
                # This is a placeholder - would need depth camera for accurate measurements
                distance = self._estimate_distance(width, height)
                
                detections.append({
                    'class': self.class_names[cls],
                    'confidence': conf,
                    'bbox': [x1, y1, x2, y2],
                    'center': [center_x, center_y],
                    'distance': distance
                })
        
        return detections
    
    def _estimate_distance(self, width: float, height: float) -> float:
        """
        Estimate the distance to an object based on its size in the image.
        This is a simplified estimation and would need calibration for real-world use.
        
        Args:
            width: Width of the bounding box
            height: Height of the bounding box
            
        Returns:
            Estimated distance in meters
        """
        # Average size of common objects in meters
        avg_object_size = 0.5
        
        # Focal length (placeholder value)
        focal_length = 1000
        
        # Calculate distance using similar triangles
        # distance = (actual_size * focal_length) / pixel_size
        pixel_size = max(width, height)
        distance = (avg_object_size * focal_length) / pixel_size
        
        return distance
    
    def get_object_descriptions(self, detections: List[Dict]) -> List[str]:
        """
        Generate natural language descriptions of detected objects.
        
        Args:
            detections: List of detected objects
            
        Returns:
            List of object descriptions
        """
        descriptions = []
        for det in detections:
            distance_str = f"{det['distance']:.1f} meters away" if det['distance'] > 0 else "nearby"
            descriptions.append(
                f"{det['class']} ({det['confidence']:.0%} confidence) {distance_str}"
            )
        return descriptions 