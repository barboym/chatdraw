



from typing import List, Tuple
import numpy as np
import itertools


def sliced_wasserstein_distance(X, Y, num_projections=100):
    rng = np.random.default_rng()
    directions = rng.normal(size=(num_projections, 2))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    sw_dist = 0.0
    for d in directions:
        proj_X = X @ d
        proj_Y = Y @ d
        proj_X.sort()
        proj_Y.sort()
        min_len = min(len(proj_X), len(proj_Y))
        sw_dist += np.mean(np.abs(proj_X[:min_len] - proj_Y[:min_len]))
    return sw_dist / num_projections


def get_drawing_score(user_points: List[List[Tuple[int, int]]], system_points: List[List[Tuple[int, int]]]) -> float:
    # Stroke count difference
    stroke_count_diff = abs(len(user_points) - len(system_points))
    
    user = np.array(list(itertools.chain.from_iterable(user_points))).astype(float)
    system = np.array(list(itertools.chain.from_iterable(system_points))).astype(float)

    system-=system.mean(0,keepdims=True)
    user-=user.mean(0,keepdims=True)
    
    max_val = max(user.max(),system.max())
    system/=max_val
    user/=max_val
    
    sw_dist = sliced_wasserstein_distance(user, system)
    score = max(0,sw_dist-(stroke_count_diff!=0)*0.2)
    return score

    # # Align lengths
    # min_len = min(len(user_arr), len(system_arr))
    # user_arr = user_arr[:min_len]
    # system_arr = system_arr[:min_len]

    # # Remove overall shift by centering
    # user_centered = user_arr - np.mean(user_arr, axis=0)
    # system_centered = system_arr - np.mean(system_arr, axis=0)

    # # Average point distance
    # avg_dist = np.mean(np.linalg.norm(user_centered - system_centered, axis=1))

    # # Combine metrics (example: penalize stroke count difference and add avg distance)
    # score = max(0.0, 1.0 - (stroke_count_diff * 0.1 + avg_dist * 0.05))
    # return score