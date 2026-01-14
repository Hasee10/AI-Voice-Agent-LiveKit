import os
import random
import string
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from livekit import api

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow the frontend to call this server

@app.route('/get_token')
def get_token():
    # 1. Generate a random unique room name for this specific user
    #    (This prevents users from hearing each other)
    room_name = "room-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # 2. Identify the user (Random Guest ID)
    participant_identity = "user-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    # 3. Create the Token using your API Keys
    token = api.AccessToken(
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET")
    ).with_identity(participant_identity) \
     .with_name(participant_identity) \
     .with_grants(api.VideoGrants(
         room_join=True,
         room=room_name,
     ))

    # 4. Return the token and room details to the frontend
    return jsonify({
        "token": token.to_jwt(),
        "room_name": room_name,
        "participant_name": participant_identity
    })

if __name__ == "__main__":
    # Run on port 5001 to avoid conflict with React (5173) or LiveKit default
    print("Starting Token Server on http://localhost:5001")
    app.run(port=5001, debug=True)