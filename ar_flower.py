import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import os
import urllib.request
import numpy as np
import random

# 1. Auto-download model
model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Downloading Google's Hand Landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Download complete!")

# 2. Setup MediaPipe
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# Particle System List
particles = []

def get_dynamic_color(distance, max_dist=250):
    """Shifts color from Blue (closed) to Hot Pink/Yellow (open)."""
    ratio = min(1.0, distance / max_dist)
    # HSV interpolation: H shifts, S and V stay high
    hue = 120 - int(ratio * 120)  # 120 is roughly blue/cyan in OpenCV HSV, 0 is red
    color_hsv = np.uint8([[[hue, 255, 255]]])
    color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)
    return (int(color_bgr[0][0][0]), int(color_bgr[0][0][1]), int(color_bgr[0][0][2]))

def draw_bezier_stem(img, start_pt, end_pt, color, thickness=3):
    """Draws a smooth curved stem instead of a straight line."""
    pts = []
    # Control point for the curve (bends it slightly to the side)
    ctrl_pt = (start_pt[0], end_pt[1] + 50) 
    
    for t in np.linspace(0, 1, 20):
        # Quadratic Bezier formula
        x = int((1 - t)**2 * start_pt[0] + 2 * (1 - t) * t * ctrl_pt[0] + t**2 * end_pt[0])
        y = int((1 - t)**2 * start_pt[1] + 2 * (1 - t) * t * ctrl_pt[1] + t**2 * end_pt[1])
        pts.append((x, y))
    
    for i in range(len(pts) - 1):
        cv2.line(img, pts[i], pts[i+1], color, thickness)

def draw_advanced_flower(mask, center, distance):
    """Draws the flower onto a black mask for glowing effects."""
    x, y = center
    max_petal_length = 180
    petal_length = min(max_petal_length, max(15, distance * 1.5))
    petal_width = max(8, petal_length // 4)
    
    # Get dynamic color based on how wide the fingers are
    primary_color = get_dynamic_color(distance)
    core_color = (255, 255, 255) # White core

    num_petals = 10
    for i in range(num_petals):
        angle = (i * 360) / num_petals
        # Inner glowing petal
        cv2.ellipse(mask, (int(x), int(y)), (int(petal_length), int(petal_width)), 
                    angle, 0, 360, primary_color, -1)
        # Outer bright outline
        cv2.ellipse(mask, (int(x), int(y)), (int(petal_length), int(petal_width)), 
                    angle, 0, 360, core_color, 2)
        
    # Center pollen bulb
    cv2.circle(mask, (int(x), int(y)), max(8, int(distance // 6)), (0, 255, 255), -1)
    return primary_color

def update_and_draw_particles(img, center, distance, color):
    """Spawns and animates floating pollen particles."""
    # Spawn new particles randomly if hands are somewhat open
    if distance > 30 and random.random() > 0.5:
        particles.append({
            'x': center[0] + random.randint(-40, 40),
            'y': center[1] + random.randint(-40, 40),
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-5, -1),
            'life': 255, # Alpha/Life
            'color': color
        })
    
    # Update and draw
    for p in particles[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 10 # Fade out speed
        
        if p['life'] <= 0:
            particles.remove(p)
        else:
            size = max(1, int(p['life'] / 50))
            cv2.circle(img, (int(p['x']), int(p['y'])), size, p['color'], -1)


# 3. Start Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    
    # Create a blank black image for our glowing elements
    overlay_mask = np.zeros_like(image)
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            thumb_tip = hand_landmarks[4]
            index_tip = hand_landmarks[8]

            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)

            distance = math.hypot(ix - tx, iy - ty)
            mid_x, mid_y = (tx + ix) // 2, (ty + iy) // 2

            flower_color = get_dynamic_color(distance)

            # 1. Draw organic curved stem
            draw_bezier_stem(image, (w // 2, h), (mid_x, mid_y), (100, 200, 100), 4)

            # 2. Draw flower onto the black mask
            draw_advanced_flower(overlay_mask, (mid_x, mid_y), distance)

            # 3. Spawn floating particles
            update_and_draw_particles(image, (mid_x, mid_y), distance, flower_color)

            # Draw minimal UI lines
            cv2.line(image, (tx, ty), (ix, iy), (255, 255, 255), 1)
            cv2.circle(image, (tx, ty), 4, (255, 255, 255), -1)
            cv2.circle(image, (ix, iy), 4, (255, 255, 255), -1)
            
            normalized_dist = round(distance / w, 2)
            cv2.putText(image, f"Bloom: {normalized_dist}", (mid_x + 30, mid_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, flower_color, 2)

    # 4. Apply the Holographic Glow (Blur the mask and add to original image)
    glow_strength = cv2.GaussianBlur(overlay_mask, (21, 21), 0)
    # Combine original image, the sharp mask, and the blurred glow
    image = cv2.addWeighted(image, 1.0, overlay_mask, 0.8, 0)
    image = cv2.addWeighted(image, 1.0, glow_strength, 1.5, 0)

    cv2.imshow('Advanced AR Generative Flower', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()