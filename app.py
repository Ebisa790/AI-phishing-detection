from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from feature_extraction import extract_features
import os

app = Flask(__name__)
CORS(app)

# Load model safely
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)

@app.route('/')
def home():
    return "AI Phishing Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data['url']

        if len(url) < 5:
            return jsonify({"error": "Invalid URL"}), 400

        features = extract_features(url)

        prediction = model.predict([features])[0]
        prob = model.predict_proba([features])[0][1]

        # 🔥 smarter classification
        if prob > 0.8:
            result = "Phishing"
        elif prob > 0.5:
            result = "Suspicious"
        else:
            result = "Safe"

        return jsonify({
            "result": result,
            "confidence": round(prob * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))