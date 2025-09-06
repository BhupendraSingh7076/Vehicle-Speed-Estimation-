import math
import time

class SpeedEstimator:
    def __init__(self, fps=30, scale=0.05):
        """
        :param fps: Frames per second of video.
        :param scale: Conversion factor (pixels → meters).
                      Adjust based on camera calibration.
        """
        self.fps = fps
        self.scale = scale
        self.prev_positions = {}  # {id: (x_center, y_center, timestamp)}

    def calculate(self, tracked_detections):
        """
        Calculate speed for tracked vehicles.
        Returns a list of results with IDs and speeds.
        """
        results = []
        current_time = time.time()

        for xyxy, track_id in zip(tracked_detections.xyxy, tracked_detections.tracker_id):
            if track_id is None:
                continue

            # get center point of bounding box
            x1, y1, x2, y2 = xyxy
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            if track_id in self.prev_positions:
                prev_x, prev_y, prev_time = self.prev_positions[track_id]

                # distance in pixels
                dist_pixels = math.sqrt((cx - prev_x) ** 2 + (cy - prev_y) ** 2)

                # convert to meters
                dist_meters = dist_pixels * self.scale

                # time elapsed
                dt = current_time - prev_time
                if dt > 0:
                    speed = dist_meters / dt * 3.6  # m/s → km/h
                else:
                    speed = 0
            else:
                speed = 0

            # update memory
            self.prev_positions[track_id] = (cx, cy, current_time)

            results.append({
                "id": int(track_id),
                "speed_kmh": round(speed, 2),
                "position": (cx, cy)
            })

        return results
