import pandas as pd
from feature_extraction import extract_features
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import joblib

print("Extracting features...")

# Load dataset (your URLs + labels)
data = pd.read_csv("dataset.csv")  # must have: url,label

X = []
y = []

for index, row in data.iterrows():
    features = extract_features(row['url'])
    X.append(features)
    y.append(row['label'])

print("Training model...")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=2
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")