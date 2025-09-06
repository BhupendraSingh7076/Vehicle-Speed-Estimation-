import supervision as sv

class VehicleTracker:
    def __init__(self):
        """
        Initialize tracker for assigning unique IDs to vehicles.
        """
        self.tracker = sv.ByteTrack()

    def update(self, detections):
        """
        Update tracker with current frame detections.
        Returns tracked detections with IDs.
        """
        tracked = self.tracker.update_with_detections(detections)
        return tracked
