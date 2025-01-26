# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# import io

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load your trained model
# model = tf.keras.models.load_model('emotiondetector.h5')  # Adjust the path to your model

# # Define the moods based on your model's output
# moods = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# @app.route('/detect-mood', methods=['POST'])
# def detect_mood():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'No image selected'}), 400

#     # Read the image
#     image = Image.open(io.BytesIO(file.read()))
#     image = image.convert('L')  # Convert to grayscale
#     image = image.resize((48, 48))  # Resize to match your model input
#     image_array = np.array(image) / 255.0  # Normalize the image
#     input_tensor = np.expand_dims(image_array, axis=0)  # Add batch dimension

#     # Make predictions
#     predictions = model.predict(input_tensor)
#     mood_index = np.argmax(predictions)  # Get the index of the highest probability
#     detected_mood = moods[mood_index]

#     return jsonify({'mood': detected_mood})

# if __name__ == '__main__':
#     app.run(port=3010)

# app.py (Backend)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from keras.models import load_model
# import base64
# import numpy as np
# import cv2

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load your custom emotion detection model
# model = load_model('C://Music_react//backend//emotiondetector.h5')

# # Updated emotion labels
# labels = {
#     0: 'angry',
#     1: 'disgust',
#     2: 'fear',
#     3: 'happy',
#     4: 'neutral',
#     5: 'sad',
#     6: 'surprise'
# }

# @app.route('/detect_emotion', methods=['POST'])
# def detect_emotion():
#     data = request.json['image']
#     img_data = base64.b64decode(data.split(',')[1])
#     img_array = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#     # Convert to grayscale if needed (if your model expects grayscale images)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     img_resized = cv2.resize(img_gray, (48, 48))  # Resize to model's input size
#     img_normalized = img_resized / 255.0  # Normalize if needed
#     img_reshaped = np.reshape(img_normalized, (1, 48, 48, 1))  # Reshape for model input (batch_size, height, width, channels)

#     # Predict emotion using the custom model
#     predictions = model.predict(img_reshaped)

#     print("Predictions:", predictions)  # Debugging line
#     print("Predictions shape:", predictions.shape)  # Debugging line

#     emotion_index = np.argmax(predictions[0])  # Get the index of the highest prediction score

#     # Map index to emotion label
#     if emotion_index in labels:
#         emotion_label = labels[emotion_index]
#     else:
#         emotion_label = 'Unknown'  # Fallback in case of an invalid index

#     return jsonify({'emotion': emotion_label})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import base64
import numpy as np
import cv2
import os
import requests

from deepface import DeepFace  # Import DeepFace
from transformers import pipeline



app = Flask(__name__)
CORS(app)  

model = load_model('C://Music_react//backend//emotiondetector1.h5')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


# @app.route('/detect_emotion', methods=['POST'])
# def detect_emotion():
#     data = request.json['image']
#     img_data = base64.b64decode(data.split(',')[1])
#     img_array = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#     # Convert to grayscale if needed (if your model expects grayscale images)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     img_resized = cv2.resize(img_gray, (48, 48))  # Resize to model's input size
#     img_normalized = img_resized / 255.0  # Normalize if needed
#     img_reshaped = np.reshape(img_normalized, (1,  48, 48, 1))  # Reshape for model input (batch_size, height, width, channels)

#     # Predict emotion using the custom model
#     predictions = model.predict(img_reshaped)

#     print("Predictions:", predictions)  # Debugging line
#     print("Predictions shape:", predictions.shape)  # Debugging line

#     emotion_index = np.argmax(predictions[0])  # Get the index of the highest prediction score

#     # Map index to emotion label
#     if emotion_index in labels:
#         emotion_label = labels[emotion_index]
#     else:
#         emotion_label = 'Unknown'  # Fallback in case of an invalid index


# def detect_emotion():
#     data = request.json['image']
#     img_data = base64.b64decode(data.split(',')[1])
#     img_array = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#     # Convert to RGB for DeepFace (DeepFace expects RGB images)
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # Analyze the image with DeepFace
#     try:
#         deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
#         emotion_label = deepface_result[0]['dominant_emotion']
#     except Exception as e:
#         emotion_label = 'Unknown'
#         print("Error with DeepFace:", e)

#     # Get a song suggestion based on the detected mood
#     song_suggestion = get_song_suggestion(emotion_label)

#     return jsonify({'emotion': emotion_label, 'song': song_suggestion})

#     # deepface_result = DeepFace.analyze(img_path=img, enforce_detection=False)
#     # deepface_emotion = deepface_result[0]['dominant_emotion'] if deepface_result else 'Unknown'

    # if emotion_label == 'Unknown':
    #     try:
    #         # Convert to RGB for DeepFace (DeepFace expects RGB images)
    #         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #         # Analyze the image with DeepFace
    #         deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
    #         emotion_label = deepface_result[0]['dominant_emotion']
    #     except Exception as e:
    #         emotion_label = 'Unknown'
    #         print("Error with DeepFace:", e)


    # # Get a song suggestion based on the detected mood
    # song_suggestion = get_song_suggestion(emotion_label)

    # return jsonify({'emotion': emotion_label, 'song': song_suggestion})

# @app.route('/detect_emotion', methods=['POST'])
# def detect_emotion():
#     data = request.json['image']
#     if not data:
#         return jsonify({'error': 'No image data provided'}), 400
#     img_data = base64.b64decode(data.split(',')[1])
#     img_array = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=5)

#     if len(faces) == 0:
#         return jsonify({'emotion': 'No face detected', 'confidence': 0.0, 'song': None})
    

#     x, y, w, h = faces[0]
#     face = img_gray[y:y + h, x:x + w]
#     face_resized = cv2.resize(face, (48, 48))
#     face_normalized = face_resized / 255.0
#     face_reshaped = np.reshape(face_normalized, (1, 48, 48, 1))

#     # Predict emotion using your custom model
#     predictions_custom = model.predict(face_reshaped)
#     custom_emotion_index = np.argmax(predictions_custom[0])
#     custom_emotion_label = labels.get(custom_emotion_index, 'Unknown')
#     custom_emotion_confidence = float(predictions_custom[0][custom_emotion_index] * 100 ) # Convert to percentage

#     # Prepare image for DeepFace
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # Predict emotion using DeepFace
#     try:
#         deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
#         deepface_emotion_label = deepface_result[0]['dominant_emotion']
#         deepface_emotion_confidence = float(deepface_result[0]['emotion'][deepface_emotion_label])  # Get confidence
#     except Exception as e:
#         deepface_emotion_label = 'Unknown'
#         deepface_emotion_confidence = 0.0
#         print("Error with DeepFace:", e)

#     # Determine the final prediction
#     if custom_emotion_label == deepface_emotion_label:
#         final_emotion_label = custom_emotion_label
#         final_confidence = max(custom_emotion_confidence, deepface_emotion_confidence)
#     else:
#         if custom_emotion_confidence > deepface_emotion_confidence:
#             final_emotion_label = custom_emotion_label
#             final_confidence = custom_emotion_confidence
#         else:
#             final_emotion_label = deepface_emotion_label
#             final_confidence = deepface_emotion_confidence

#     # Get a song suggestion based on the final predicted mood
#     song_suggestion = get_song_suggestion(final_emotion_label)

#     return jsonify({
#         'emotion': final_emotion_label,
#         'confidence': final_confidence,
#         'song': song_suggestion
#     })


@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    data = request.json['image']
    if not data:
        return jsonify({'error': 'No image data provided'}), 400

    img_data = base64.b64decode(data.split(',')[1])
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Convert to RGB for DeepFace (DeepFace expects RGB images)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Predict emotion using DeepFace
    try:
        deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
        emotion_label = deepface_result[0]['dominant_emotion']
        emotion_confidence = float(deepface_result[0]['emotion'][emotion_label])  # Get confidence
    except Exception as e:
        emotion_label = 'Unknown'
        emotion_confidence = 0.0
        print("Error with DeepFace:", e)

    mood_mapping = {
        'happy': 'happy',
        'sad': 'sad',
        'angry': 'angry',
        'fear': 'fear',
        'disgust': 'disgust',
        'surprise': 'surprise',
        'neutral': 'neutral',
        # Add mappings for sexy and romantic moods
        'romantic': 'romantic',  # You can map 'happy' or 'surprise' to 'romantic' if needed
        'sexy': 'sexy'           # You can map 'happy' or 'surprise' to 'sexy' if needed
    }
    if emotion_label in mood_mapping:
        final_mood = mood_mapping[emotion_label]
    else:
        final_mood = 'neutral'  # Default to neutral if no mapping exists

    # Get a song suggestion based on the detected mood
    song_suggestion = get_song_suggestion(emotion_label)

    return jsonify({
        'emotion': emotion_label,
        'confidence': emotion_confidence,
        'song': song_suggestion
    })


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
    custom_emotion_confidence = float(predictions[0][emotion_index] * 100 ) # Convert to percentage

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

     # Predict emotion using DeepFace
    try:
        deepface_result = DeepFace.analyze(img_path=img_rgb, actions=['emotion'], enforce_detection=False)
        deepface_emotion_label = deepface_result[0]['dominant_emotion']
        deepface_emotion_confidence = float(deepface_result[0]['emotion'][deepface_emotion_label])  # Get confidence
    except Exception as e:
        deepface_emotion_label = 'Unknown'
        deepface_emotion_confidence = 0.0
        print("Error with DeepFace:", e)

    # Determine the final prediction
    if emotion_label == deepface_emotion_label:
        final_emotion_label = emotion_label
        final_confidence = max(custom_emotion_confidence, deepface_emotion_confidence)
    else:
        if custom_emotion_confidence > deepface_emotion_confidence:
            final_emotion_label = emotion_label
            final_confidence = custom_emotion_confidence
        else:
            final_emotion_label = deepface_emotion_label
            final_confidence = deepface_emotion_confidence

    # Get a song suggestion based on the detected mood
    song_suggestion = get_song_suggestion(final_emotion_label)

    return jsonify({'emotion': final_emotion_label, 'song': song_suggestion})



# CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "supports_credentials": True}})
# Load a conversational model
chatbot_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def detect_mood(user_input):
    """Simple mood detection based on keywords in the input."""
    user_input = user_input.lower()
    if any(word in user_input for word in ["happy", "excited", "joyful", "great"]):
        return "happy"
    elif any(word in user_input for word in ["sad", "down", "depressed", "unhappy"]):
        return "sad"
    elif any(word in user_input for word in ["angry", "mad", "frustrated"]):
        return "angry"
    elif any(word in user_input for word in ["calm", "relaxed", "peaceful"]):
        return "calm"
    else:
        return "neutral"
    
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user input from JSON body
        user_input = request.json.get('input')
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        # Generate chatbot response
        bot_response = chatbot_pipeline(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
        mood = detect_mood(user_input)

        # Return JSON response
        return jsonify({
            'response': bot_response,
            'mood': mood
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)