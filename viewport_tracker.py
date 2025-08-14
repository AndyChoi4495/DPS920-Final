# viewport_tracker.py
"""
Viewport tracking functions for creating a smooth "virtual camera".
"""

import cv2
import numpy as np


def calculate_region_of_interest(motion_boxes, frame_shape):
    """
    Calculate the primary region of interest based on motion boxes.

    Args:
        motion_boxes: List of motion detection bounding boxes
        frame_shape: Shape of the video frame (height, width)

    Returns:
        Tuple (x, y, w, h) representing the region of interest center point and dimensions
    """
    # TODO: Implement region of interest calculation
    # 1. Choose a strategy for determining the main area of interest
    #    - You could use the largest motion box
    #    - Or combine nearby boxes
    #    - Or use a weighted average of all motion boxes
    # 2. Return the coordinates of the chosen region

    # Example starter code:
    if not motion_boxes:
        # If no motion is detected, use the center of the frame
        height, width = frame_shape[:2]
        return (width // 2, height // 2, 0, 0)

    # Your implementation here
    # Strategy: use weighted average of box centers based on area
    total_area = 0
    sum_x = 0
    sum_y = 0

    for (x, y, w, h) in motion_boxes:
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        sum_x += cx * area
        sum_y += cy * area
        total_area += area

    avg_cx = int(sum_x / total_area)
    avg_cy = int(sum_y / total_area)

    return (avg_cx, avg_cy, 0, 0)


def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
    """
    Track viewport position across frames with smoothing.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_size: Tuple (width, height) of the viewport
        smoothing_factor: Factor for smoothing viewport movement (0-1)
                          Lower values create smoother movement

    Returns:
        List of viewport positions for each frame as (x, y) center coordinates
    """
    # TODO: Implement viewport tracking with smoothing
    # 1. For each frame, determine the region of interest based on motion_results
    # 2. Apply smoothing to avoid jerky movements
    #    - Use previous viewport positions to smooth the movement
    #    - Consider implementing a simple exponential moving average
    #    - Or a more advanced approach like Kalman filtering
    # 3. Ensure the viewport stays within the frame boundaries
    # 4. Return the list of viewport positions for all frames

    # Example starter code:
    viewport_positions = []

    # Initialize with center of first frame if available
    if frames:
        height, width = frames[0].shape[:2]
        prev_x, prev_y = width // 2, height // 2
    else:
        return []

    vw, vh = viewport_size

    # Your implementation here
    for i in range(len(frames)):
        # Step 1: get ROI center
        cx, cy, _, _ = calculate_region_of_interest(motion_results[i], frames[i].shape)

        # Step 2: apply exponential moving average for smoothing
        smoothed_x = int((1 - smoothing_factor) * prev_x + smoothing_factor * cx)
        smoothed_y = int((1 - smoothing_factor) * prev_y + smoothing_factor * cy)

        # Step 3: clamp to stay within frame
        smoothed_x = max(vw // 2, min(width - vw // 2, smoothed_x))
        smoothed_y = max(vh // 2, min(height - vh // 2, smoothed_y))

        viewport_positions.append((smoothed_x, smoothed_y))

        # Step 4: update previous
        prev_x, prev_y = smoothed_x, smoothed_y

    return viewport_positions
