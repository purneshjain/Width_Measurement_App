import os
from twilio.rest import Client

# Retrieve Twilio credentials from environment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send a message
message = client.messages.create(
    body="Hello from Streamlit!",
    from_=twilio_phone_number,
    to="recipient_phone_number"
)

# Confirm that the message was sent
print(message.sid)
