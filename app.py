from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import hashlib
import mysql.connector
from feature_extraction import extract_features

app = Flask(__name__)
CORS(app)

# Database Credentials
DB_CONFIG = {
    'user': 'if0_41692218',
    'password': 'Ebba2241',
    'host': 'sql205.infinityfree.com',
    'database': 'if0_41692218_phishing_db'
}

# Load Model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/', methods=['GET'])
def home():
    return "PhishGuard AI Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data['url']
    url_hash = hashlib.sha256(url.encode()).hexdigest()

    try:
        # 1. Check Cache
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT verdict, confidence FROM link_analysis WHERE url_hash = %s", (url_hash,))
        cached = cursor.fetchone()

        if cached:
            cursor.close(); conn.close()
            return jsonify({"result": cached['verdict'], "confidence": float(cached['confidence']), "cached": True})

        # 2. Analyze if not cached
        features = extract_features(url)
        prob = model.predict_proba(np.array([features]))[0][1]

        # Classification Logic
        if prob > 0.8:
            result = "Phishing"
        elif prob > 0.5:
            result = "Suspicious"
        else:
            result = "Safe"
        
        confidence = round(float(prob) * 100, 2)

        # 3. Save to Database
        cursor.execute(
            "INSERT INTO link_analysis (url, url_hash, verdict, confidence, status) VALUES (%s, %s, %s, %s, 'completed')",
            (url, url_hash, result, confidence)
        )
        conn.commit()
        cursor.close(); conn.close()

        return jsonify({"result": result, "confidence": confidence, "cached": False})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))