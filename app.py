from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from feature_extraction import extract_features

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model = joblib.load("model.pkl")
    print("Model loaded successfully!")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model.pkl. {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url')
        
        # Extract features
        features = extract_features(url)
        
        # Convert to 2D array - 
        features_array = np.array([features]) 
        
        # Get probability
        prob = model.predict_proba(features_array)[0][1]


        if prob > 0.7:
            result = "Phishing"
        elif prob > 0.4:
            result = "Suspicious"
        else:
            result = "Safe"

        return jsonify({
            "result": result,
            "confidence": round(float(prob) * 100, 2)
        })

    # --- UPDATE IN app.py ---
    except Exception as e:
     import traceback
     errors = traceback.format_exc() # This gets the full error details
     print(errors) # This shows in Render Logs
     return jsonify({"error": str(e), "details": errors}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phishing Detection API is Running!"

if __name__ == '__main__':
    app.run()