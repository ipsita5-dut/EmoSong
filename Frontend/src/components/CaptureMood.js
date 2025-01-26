// // CaptureMood.js
// import React, { useEffect, useRef, useState } from 'react';
// import '../styles/captureMood.css'; // Import your CSS file
// import * as faceapi from 'face-api.js';

// const CaptureMood = () => {
//   const videoRef = useRef(null);
//   const [detectedMood, setDetectedMood] = useState("None");
//   const [songSuggestion, setSongSuggestion] = useState(null);

//   const loadModels = async () => {
//     if (typeof window.faceapi === 'undefined') {
//       console.error("faceapi is not defined. Make sure face-api.js is loaded correctly.");
//       return;
//     }

//     try {
//       await window.faceapi.nets.tinyFaceDetector.loadFromUri("/models");
//       await window.faceapi.nets.faceExpressionNet.loadFromUri("/models");
//       console.log("Models loaded successfully");
//     } catch (error) {
//       console.error("Error loading models:", error);
//     }
//   };

//   const startWebcam = async () => {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//       videoRef.current.srcObject = stream;
//       videoRef.current.onloadedmetadata = () => {
//         videoRef.current.play();
//       };
//         } catch (error) {
//       console.error("Error accessing webcam:", error);
//       alert("Could not access the webcam. Please check your permissions.");
//     }
//   };

//   const captureMood = async () => {
//     if (typeof window.faceapi === 'undefined') {
//       console.error("faceapi is not defined. Make sure face-api.js is loaded correctly.");
//       return;
//     }

//     try {
//       const detections = await window.faceapi
//         .detectAllFaces(videoRef.current, new window.faceapi.TinyFaceDetectorOptions())
//         .withFaceExpressions();

//       if (detections.length > 0) {
//         const canvasElement = document.createElement('canvas');
//         canvasElement.width = videoRef.current.videoWidth;
//         canvasElement.height = videoRef.current.videoHeight;
//         const context = canvasElement.getContext('2d');
//         context.drawImage(videoRef.current, 0, 0, canvasElement.width, canvasElement.height);

//         canvasElement.toBlob(async (blob) => {
//           const formData = new FormData();
//           formData.append('image', blob);

//           try {
//             const response = await fetch('http://localhost:3010/detect-mood', {
//               method: 'POST',
//               body: formData,
//             });
//             const data = await response.json();

//             if (data && data.mood) {
//               setDetectedMood(data.mood.charAt(0).toUpperCase() + data.mood.slice(1));
//             } else {
//               setDetectedMood("Mood not detected");
//             }
//           } catch (error) {
//             console.error("Error fetching mood detection:", error);
//             setDetectedMood("Error detecting mood");
//           }
//         }, 'image/jpeg');
//       } else {
//         setDetectedMood("No face detected");
//       }
//     } catch (error) {
//       console.error("Error capturing mood:", error);
//     }
//   };

//   useEffect(() => {
//     loadModels();
//     startWebcam();
//   }, []);

//   return (
//     <div>
//       <h1>Capture Your Mood</h1>
//       <div className="webcam-container">
//         <video ref={videoRef} autoPlay width="640" height="480"></video>
//         <button id="capture-button" onClick={captureMood}>Capture Mood</button>
//       </div>
//       <div id="mood-result">
//         <h2>Detected Mood: <span id="detected-mood">{detectedMood}</span></h2>
//       </div>
//     </div>
//   );
// };

// export default CaptureMood;

import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
// import '../styles/captureMood.css';
import '../styles/captureMood.css';

const CaptureMood = () => {
  const videoRef = useRef(null);
  const [emotion, setEmotion] = useState('');
  const [song, setSong] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const startVideo = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
      videoRef.current.srcObject = stream;
    };

    startVideo();
  }, []);

  const captureImage = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);

    // Send captured image to backend for emotion detection
    const dataURL = canvas.toDataURL('image/jpeg');
    try {
      const response = await axios.post('http://localhost:5000/detect_emotion', { image: dataURL });
      setEmotion(response.data.emotion);
      setSong(response.data.song);
      setShowModal(true);
    } catch (error) {
      console.error("Error detecting emotion:", error);
      setEmotion('Error detecting emotion');
    }
  };

  const closeModal = () => {
    setShowModal(false);
  };
  return (
    <div>
      <video ref={videoRef} autoPlay muted />
      <button className="capture-btn" onClick={captureImage}>Detect Emotion</button>
      <h2>Detected Emotion: {emotion}</h2>

      {showModal && song && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <h2>Song Recommendation</h2>
            <p>{song.song_name} by {song.artist_name}</p>

            <img src={song.cover_url} alt={`${song.song_name} cover`} width="200" />
            <p>Artist: {song.artist_name}</p>
            <p>Album: {song.album_name}</p> {/* Display album name */}

            <a href={song.spotify_url} target="_blank" rel="noopener noreferrer">
              <button>Play on Spotify</button>
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default CaptureMood;
