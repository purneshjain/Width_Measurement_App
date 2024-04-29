import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
import cv2
import numpy as np
import logging
import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Function to get ICE servers using Twilio
def get_ice_servers():
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        token = client.tokens.create()
        return token.ice_servers
    except KeyError:
        logger.warning("Twilio credentials are not set. Using a free STUN server from Google.")
        return [{"urls": ["stun:stun.l.google.com:19302"]}]
    except TwilioRestException as e:
        logger.warning(f"Twilio API access error: {e}. Using a free STUN server from Google.")
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

# Video processing class
class WidthMeasurementProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # Process the image here (add your image processing code)
        distance = 10  # Example distance value
        cv2.putText(img, f"Distance: {distance}mm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Main app function
def main():
    st.title("Real-Time Width Measurement")
    st.write("This app measures the width of objects in real-time using your webcam.")

    # Get ICE servers
    ice_servers = get_ice_servers()

    # Streamlit-WebRTC component
    webrtc_ctx = webrtc_streamer(
        key="width-measurement",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": ice_servers},
        video_processor_factory=WidthMeasurementProcessor
    )

if _name_ == "_main_":
    main()
