const fs = require('fs');

function verifyTFJSModel(filePath) {
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    // Check for required keys
    if (data.modelTopology && data.weightsManifest) {
      console.log("The JSON file is in TensorFlow.js format.");
      return true;
    } else {
      console.log("The JSON file is NOT in TensorFlow.js format.");
      return false;
    }
  } catch (err) {
    console.error("Error reading or processing the file:", err);
    return false;
  }
}

// Path to your emotiondetector.json file
const filePath = "emotiondetector.json";
verifyTFJSModel(filePath);
