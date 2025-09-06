import pandas as pd
import cv2
import os

def save_results(results, output_csv="outputs/vehicle_speeds.csv"):
    """
    Save vehicle speed data into CSV.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df = pd.DataFrame(results)
    if not df.empty:
        if not os.path.exists(output_csv):
            df.to_csv(output_csv, index=False, mode="w")
        else:
            df.to_csv(output_csv, index=False, mode="a", header=False)

def draw_annotations(frame, results):
    """
    Draw speed + ID on vehicles.
    """
    for r in results:
        cx, cy = r["position"]
        text = f"ID {r['id']} | {r['speed_kmh']} km/h"
        cv2.putText(frame, text, (cx, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
    return frame
