"""
Dynamic Time Warping (DTW) & Elastic Pitch Delta Engine for Song Lab.
Aligns student pitch contours against canonical raga trajectories,
computing cent-by-cent deviation, intonational purity, and diagnostic heatmap bands.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np


def compute_pitch_dtw(
    user_cents: np.ndarray,
    ideal_cents: np.ndarray,
    hop_sec: float = 0.01,
) -> Dict:
    """
    Computes elastic DTW alignment between user pitch curve and ideal raga trajectory.
    Returns warped paths, cent-by-cent deltas, and diagnostic summary metrics.
    """
    if user_cents is None or len(user_cents) == 0:
        return {"error": "Empty user pitch trajectory"}
    if ideal_cents is None or len(ideal_cents) == 0:
        return {"error": "Empty ideal target trajectory"}

    # Mask NaNs or zero-unvoiced
    u_arr = np.nan_to_num(user_cents, nan=0.0).astype(float)
    i_arr = np.nan_to_num(ideal_cents, nan=0.0).astype(float)

    n = len(u_arr)
    m = len(i_arr)

    # In case arrays are too large for full O(n*m), cap or downsample if needed
    step_u = max(1, n // 300)
    step_i = max(1, m // 300)
    u_sub = u_arr[::step_u]
    i_sub = i_arr[::step_i]

    sn, sm = len(u_sub), len(i_sub)

    # Dynamic Programming Matrix
    D = np.full((sn + 1, sm + 1), np.inf)
    D[0, 0] = 0.0

    # Local distance matrix (sub-cent absolute difference)
    cost_matrix = np.abs(u_sub[:, None] - i_sub[None, :])

    for i in range(1, sn + 1):
        for j in range(1, sm + 1):
            cost = cost_matrix[i - 1, j - 1]
            D[i, j] = cost + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])

    # Backtrack optimal warping path
    i, j = sn, sm
    path = []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        steps = [
            (D[i - 1, j - 1], i - 1, j - 1),
            (D[i - 1, j], i - 1, j),
            (D[i, j - 1], i, j - 1),
        ]
        steps.sort(key=lambda x: x[0])
        _, i, j = steps[0]

    path.reverse()

    # Cent deltas along aligned path
    aligned_user = np.array([u_sub[p[0]] for p in path])
    aligned_ideal = np.array([i_sub[p[1]] for p in path])
    delta_cents = aligned_user - aligned_ideal

    abs_deltas = np.abs(delta_cents)
    mad = float(np.mean(abs_deltas)) if len(abs_deltas) else 0.0
    rmse = float(np.sqrt(np.mean(delta_cents ** 2))) if len(delta_cents) else 0.0
    
    # Just Intonation pure window: <= 15 cents
    purity_pct = float(np.mean(abs_deltas <= 15.0) * 100.0) if len(abs_deltas) else 0.0
    acceptable_pct = float(np.mean(abs_deltas <= 35.0) * 100.0) if len(abs_deltas) else 0.0
    
    # Intonation score in [0, 100]
    alignment_score = max(0.0, min(100.0, 100.0 * np.exp(-mad / 50.0)))

    # Construct downsampled stream for UI visualization
    ui_stream = []
    subsample_rate = max(1, len(path) // 60)
    for idx in range(0, len(path), subsample_rate):
        p_u, p_i = path[idx]
        d = float(delta_cents[idx])
        # Dark room aesthetic zones:
        # Green (within pure 15c window), Amber (15-35c intonation drift), Red (>35c severe deviation)
        zone = "green" if abs(d) <= 15.0 else ("amber" if abs(d) <= 35.0 else "red")
        ui_stream.append({
            "t_user": round(float(p_u * step_u * hop_sec), 3),
            "user_cents": round(float(u_sub[p_u]), 1),
            "ideal_cents": round(float(i_sub[p_i]), 1),
            "delta_cents": round(d, 1),
            "zone": zone,
        })

    return {
        "metrics": {
            "alignment_score": round(alignment_score, 1),
            "mean_absolute_deviation_cents": round(mad, 2),
            "rmse_cents": round(rmse, 2),
            "intonation_purity_pct": round(purity_pct, 1),
            "acceptable_pct": round(acceptable_pct, 1),
            "total_aligned_frames": len(path),
        },
        "alignment_stream": ui_stream,
    }
