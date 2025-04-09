import math
import cv2
import numpy as np
import requests
import pygame
from ultralytics import YOLO

# Initialize the pygame mixer
pygame.mixer.init()


sound_file_path = "C:/Users/ADMIN/Downloads/alarm.mp3"

# Dictionary mapping class IDs to object names
object_names = {
    0: 'Knife',
    1: 'Scissors',
    3: 'Coin'
}

# Distance threshold in pixels
DISTANCE_THRESHOLD = 150

# Function to play alarm sound using pygame.mixer
def play_alarm_sound():
    try:
        pygame.mixer.music.load(sound_file_path)  # Load the sound file
        pygame.mixer.music.play()  # Play the sound
    except Exception as e:
        print(f"Error playing alarm sound: {e}")

# Function to send email asynchronously to Flask server
def send_email(object_name, toddler_id, recipient_email):
    try:
        url = "http://localhost:5000/send_email"  # Flask server URL
        data = {
            "object_name": object_name,
            "toddler_id": toddler_id,
            "recipient_email": recipient_email
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("✅ Email sent successfully!")
        else:
            print(f"❌ Failed to send email: {response.text}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Load the trained YOLO model
model = YOLO("C:/Users/ADMIN/Downloads/best.pt")

# Open the webcam (change index to 1 or 2 if needed)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Run inference on the current frame
    results = model(frame)
    predictions = results[0].boxes

    # Extract bounding boxes, class IDs, and confidence scores
    boxes = predictions.xyxy.cpu().numpy()         # Bounding boxes: (x1, y1, x2, y2)
    class_ids = predictions.cls.cpu().numpy()        # Class IDs
    confidence_scores = predictions.conf.cpu().numpy() # Confidence scores

    # Store all detections with center coordinates
    detections = []
    for i in range(len(class_ids)):
        x1, y1, x2, y2 = boxes[i]
        class_id = int(class_ids[i])
        confidence = confidence_scores[i]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        detections.append({
            'class_id': class_id,
            'confidence': confidence,
            'center': (cx, cy),
            'box': (x1, y1, x2, y2)
        })

    alarm_triggered = False

    # Iterate through detections to check for toddler and dangerous objects
    for det in detections:
        if det['class_id'] == 2:  # Toddler detected (assuming toddler's class ID is 2)
            toddler_center = det['center']
            toddler_box = det['box']
            for other in detections:
                if other['class_id'] in [0, 1, 3]:  # Dangerous objects
                    cx1, cy1 = toddler_center
                    cx2, cy2 = other['center']
                    # Calculate Euclidean distance
                    distance = math.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2)
                    if distance <= DISTANCE_THRESHOLD:
                        print(f"🚨 ALARM: Toddler is near a dangerous object ({object_names.get(other['class_id'], 'Unknown')})!")
                        alarm_triggered = True
                        play_alarm_sound()
                        send_email(object_names.get(other['class_id'], 'Unknown'), 2, "fatimaahmadd038@gmail.com")  # Send email
                        break
                    # Check if the toddler and dangerous object overlap (toddler holding it)
                    x1_t, y1_t, x2_t, y2_t = toddler_box
                    x1_o, y1_o, x2_o, y2_o = other['box']
                    if (x1_t < x2_o and x2_t > x1_o and y1_t < y2_o and y2_t > y1_o):
                        print(f"🚨 ALARM: Toddler is HOLDING a dangerous object ({object_names.get(other['class_id'], 'Unknown')})!")
                        alarm_triggered = True
                        play_alarm_sound()
                        send_email(object_names.get(other['class_id'], 'Unknown'), 2, "fatimaahmadd038@gmail.com")  # Send email
                        break
            if alarm_triggered:
                break

    if not alarm_triggered:
        print("✅ No immediate danger detected. Toddler is at a safe distance.")

    # Draw bounding boxes on the frame
    for det in detections:
        x1, y1, x2, y2 = det['box']
        color = (0, 255, 0) if det['class_id'] == 2 else (255, 0, 0)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

    # Display the current frame
    cv2.imshow("MiniGuard AI - Live Camera", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()