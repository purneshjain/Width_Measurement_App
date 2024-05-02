import cv2
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import av
import numpy as np
import logging
import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from sample_utils.download import download_file
from sample_utils.turn import get_ice_servers


# Additional imports from streamlit_webrtc
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

logger = logging.getLogger(__name__)

def get_ice_servers():
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token =os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        token = client.tokens.create()
    except TwilioRestException as e:
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    return token.ice_servers

st.title("Width Measurement")

# Get ICE servers
ice_servers = get_ice_servers()

class WidthMeasurementProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # Process the image here
        # Example: Draw lines and text on the image
        distance = 10  # Example distance value
        cv2.putText(img, f"Distance: {distance}mm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add ICE servers configuration
    video_processor_factory=WidthMeasurementProcessor,
)
