from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from feature_extraction import extract_features

app = Flask(__name__)
CORS(app)

model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data['url']

    features = extract_features(url)

    prediction = model.predict([features])[0]
    prob = model.predict_proba([features])[0][1]

    result = "Phishing" if prediction == 1 else "Safe"
    confidence = round(prob * 100, 2)

    return jsonify({
        "result": result,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)