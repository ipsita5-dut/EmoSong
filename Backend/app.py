# app.py (Backend)
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import base64
import numpy as np
import cv2
import os
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your custom emotion detection model
model = load_model('C://Music_react//backend//emotiondetector1.h5')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Updated emotion labels
labels = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprise'
}
# Spotify API credentials
SPOTIFY_CLIENT_ID = '79fd69d47eb74d6d96e36e76b351dfa0'
SPOTIFY_CLIENT_SECRET = 'c5115519ccb543b095773cda41b1680d'



def get_spotify_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')
def get_song_suggestion(mood):
    access_token = get_spotify_access_token()
    if not access_token:
        return None

    # Define additional mood-based search criteria
    mood_keywords = {
        'angry': 'rock, intense',
        'disgust': 'aggressive, dark,soothing',
        'fear': 'suspense, dramatic,funny',
        'happy': 'upbeat, cheerful,romantic,love',
        'neutral': 'chill, mellow',
        'sad': 'soft, slow, melancholic',
        'surprise': 'surprising, energetic',
        'romantic': 'romantic, love',  # Romantic mood
        'sexy': 'sexy, seductive',      # Sexy mood
        'romantic_sexy': 'romantic, sexy, seductive'  # Combined mood
    
    }

    mood_query = mood_keywords.get(mood, 'upbeat')  # Default to upbeat if the mood is unknown

    search_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Use a more specific query based on mood
    query = f"{mood_query} (Bengali OR Bollywood)"
    
    params = {
        'q': query,
        'type': 'playlist',
        'limit': 10
    }

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        print("Spotify Search API Error:", response.json())
        return None

    playlists = response.json().get('playlists', {}).get('items', [])
    if not playlists:
        print(f"No playlists found for mood: {mood} with Bengali or Bollywood music")
        return None

    # Select a playlist that best matches the mood
    selected_playlist = np.random.choice(playlists)
    if 'id' not in selected_playlist:
        print("Selected playlist does not have an 'id':", selected_playlist)
        return None
    playlist_id = selected_playlist['id']

    # Fetch tracks from the selected playlist
    tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    tracks_response = requests.get(tracks_url, headers=headers)
    if tracks_response.status_code != 200:
        print("Spotify Tracks API Error:", tracks_response.json())
        return None

    tracks = tracks_response.json().get('items', [])
    if not tracks:
        print(f"No tracks found in playlist: {selected_playlist['name']}")
        return None

    # Randomly select a track from the playlist that fits the mood
    track = np.random.choice(tracks)
    song_name = track['track']['name']
    artist_name = track['track']['artists'][0]['name']
    spotify_url = track['track']['external_urls']['spotify']
    cover_url = track['track']['album']['images'][0]['url']
    album_name = track['track']['album']['name']

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "spotify_url": spotify_url,
        "album_name": album_name,
        "cover_url": cover_url  # Include the cover image URL
    }



@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_resized = cv2.resize(img_gray, (48, 48))  # Resize to model's input size
    img_normalized = img_resized / 255.0  # Normalize if needed
    img_reshaped = np.reshape(img_normalized, (1, 48, 48, 1))  # Reshape for model input (batch_size, height, width, channels)

    # Predict emotion using the custom model
    predictions = model.predict(img_reshaped)

    print("Predictions:", predictions)  # Debugging line
    print("Predictions shape:", predictions.shape)  # Debugging line

    emotion_index = np.argmax(predictions[0])  # Get the index of the highest prediction score

    # Map index to emotion label
    if emotion_index in labels:
        emotion_label = labels[emotion_index]
    else:
        emotion_label = 'Unknown'  # Fallback in case of an invalid index

    # return jsonify({'emotion': emotion_label})
    song_suggestion = get_song_suggestion(emotion_label)

    return jsonify({'emotion': emotion_label, 'song': song_suggestion})


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file to the uploads folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Perform mood detection
    img = cv2.imread(file_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (48, 48))
    img_normalized = img_resized / 255.0
    img_reshaped = np.reshape(img_normalized, (1, 48, 48, 1))

    predictions = model.predict(img_reshaped)
    emotion_index = np.argmax(predictions[0])
    emotion_label = labels.get(emotion_index, 'Unknown')
    # custom_emotion_confidence = float(predictions[0][emotion_index] * 100 ) # Convert to percentage

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

     # Predict emotion using DeepFace
    # try:
    #     deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
    #     deepface_emotion_label = deepface_result[0]['dominant_emotion']
    #     deepface_emotion_confidence = float(deepface_result[0]['emotion'][deepface_emotion_label])  # Get confidence
    # except Exception as e:
    #     deepface_emotion_label = 'Unknown'
    #     deepface_emotion_confidence = 0.0
    #     print("Error with DeepFace:", e)

    if emotion_index in labels:
        emotion_label = labels[emotion_index]
    else:
        emotion_label = 'Unknown'  # Fallback in case of an invalid index

    # Get a song suggestion based on the detected mood
    song_suggestion = get_song_suggestion(emotion_label)

    return jsonify({'emotion': emotion_label, 'song': song_suggestion})


if __name__ == '__main__':
    app.run(debug=True)
