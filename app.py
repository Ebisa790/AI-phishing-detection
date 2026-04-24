from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import traceback

app = Flask(__name__)
CORS(app)

# Load the entire Pipeline (TF-IDF + Random Forest)
try:
    model = joblib.load("model.pkl")
    print("Pipeline model loaded successfully!")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model.pkl. {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # IMPORTANT: Since we used a Pipeline, we pass the URL as a list of strings.
        # The Pipeline automatically handles the TF-IDF text conversion for us.
        prob = model.predict_proba([url])[0][1]

        # Logic for result based on phishing probability
        if prob > 0.75:
            result = "Phishing"
        elif prob > 0.45:
            result = "Suspicious"
        else:
            result = "Safe"

        return jsonify({
            "result": result,
            "confidence": round(float(prob) * 100, 2),
            "url": url
        })

    except Exception as e:
        errors = traceback.format_exc()
        print(errors)
        return jsonify({"error": str(e), "details": errors}), 500

@app.route('/', methods=['GET'])
def home():
    return "PhishGuard AI Detection API is Running!"

if __name__ == '__main__':
    # Use threaded=True for better handling of multiple requests
    app.run(debug=True, port=5000)