import supervision as sv
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt", classes=[2, 3, 5, 7]):
        """
        Initialize YOLOv8 model for vehicle detection.
        Default COCO classes:
            2 - car
            3 - motorcycle
            5 - bus
            7 - truck
        """
        self.model = YOLO(model_path)
        self.classes = classes
        self.box_annotator = sv.BoxAnnotator()

    def detect(self, frame):
        """
        Run YOLOv8 on a single frame.
        Returns detections in supervision format.
        """
        results = self.model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[detections.class_id.isin(self.classes)]
        return detections

    def annotate(self, frame, detections, labels=None):
        """
        Draw bounding boxes + labels on frame.
        """
        return self.box_annotator.annotate(scene=frame, detections=detections, labels=labels)
