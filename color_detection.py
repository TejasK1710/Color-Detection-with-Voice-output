import cv2
import numpy as np
from gtts import gTTS
import pygame
import os
import time

# Initialize Pygame for audio playback
pygame.mixer.init()

# Define color ranges in HSV format
color_ranges = {
    "Red": ([0, 100, 100], [10, 255, 255]),
    "Green": ([40, 70, 70], [80, 255, 255]),
    "Blue": ([100, 150, 0], [140, 255, 255]),
    "Yellow": ([20, 100, 100], [30, 255, 255]),
}

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not found or cannot be opened!")
    exit()

# Function to generate and play voice output
def play_audio(color_name):
    tts = gTTS(text=f"The detected color is {color_name}", lang="en")
    audio_file = "color.mp3"
    tts.save(audio_file)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    os.remove(audio_file)

# Main loop
previous_color = None
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video")
        break

    # Convert the frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect colors
    detected_color = None
    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype="uint8")
        upper_bound = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        if cv2.countNonZero(mask) > 500:  # Adjust threshold as needed
            detected_color = color_name
            break

    # Display the detected color on the frame
    if detected_color:
        cv2.putText(frame, detected_color, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Play audio only when the color changes
        if detected_color != previous_color:
            play_audio(detected_color)
            previous_color = detected_color

    # Show the video feed
    cv2.imshow("Color Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
