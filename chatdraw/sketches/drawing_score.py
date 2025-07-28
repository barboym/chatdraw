



from typing import List, Tuple
import numpy as np

def get_drawing_score(user_points: List[List[Tuple[float, float]]], system_points: List[List[Tuple[float, float]]]) -> float:
    # Stroke count difference
    stroke_count_diff = abs(len(user_points) - len(system_points))

    # Flatten strokes to points
    def flatten(points):
        return [pt for stroke in points for pt in stroke]

    user_flat = flatten(user_points)
    system_flat = flatten(system_points)

    # If no points, return 0
    if not user_flat or not system_flat:
        return 0.0

    # Convert to numpy arrays
    user_arr = np.array(user_flat)
    system_arr = np.array(system_flat)

    # Align lengths
    min_len = min(len(user_arr), len(system_arr))
    user_arr = user_arr[:min_len]
    system_arr = system_arr[:min_len]

    # Remove overall shift by centering
    user_centered = user_arr - np.mean(user_arr, axis=0)
    system_centered = system_arr - np.mean(system_arr, axis=0)

    # Average point distance
    avg_dist = np.mean(np.linalg.norm(user_centered - system_centered, axis=1))

    # Combine metrics (example: penalize stroke count difference and add avg distance)
    score = max(0.0, 1.0 - (stroke_count_diff * 0.1 + avg_dist * 0.05))
    return score