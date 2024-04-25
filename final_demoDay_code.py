import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer 
import av
import numpy as np

st.title("Width Measurement")

def callback(frame: av.VideoFrame) -> av.VideoFrame:
    # Convert video frame to an ndarray
    img = frame.to_ndarray(format="bgr24")

    # Convert the image to grayscale and apply gaussian blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Corrected function name and color conversion
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Corrected function name

    # Apply thresholding and find contours
    _, thresh = cv2.threshold(blur, 75, 255, cv2.THRESH_BINARY_INV)  # Corrected function name and threshold type
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Corrected function name and retrieval mode, and contour approximation method
    cnts = contours[0] if len(contours) == 2 else contours[1]

    min_area = 1000
    black_dots = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            black_dots.append(c)

    # Create a blank image for drawing contours
    contours_only = np.zeros_like(img)
    cv2.drawContours(contours_only, black_dots, -1, (0, 255, 0), 2)  # Corrected function name and added thickness parameter

    pxl_ratio = 16 / 160
    for row_num in range(img.shape[0] - 1):
        # Find left and right pixel coordinates for width measurement
        row = gray[row_num: row_num + 1, :]
        left_px = np.argmax(row)
        row = np.flip(row)
        right_px = img.shape[1] - np.argmax(row)
        thickness = 2
        if row_num % 100 == 0 and left_px != 0 and right_px != 0:
            # Draw a line and display the distance
            cv2.line(img, (left_px, row_num), (right_px, row_num), (0, 0, 255), thickness)
            distance = round((right_px - left_px) * pxl_ratio, 2)
            l_org = row_num - 10
            cv2.putText(img, str(distance) + "mm", (left_px, l_org), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # Corrected function name and added text font, size, and thickness
            print(distance)

    # Convert the ndarray back to a video frame
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Stream the video and apply the callback
webrtc_streamer(key="object-detection", video_frame_callback=callback)