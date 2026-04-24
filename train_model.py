import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib

def train_phishguard_model():
    print("Step 1: Loading Dataset...")
    try:
        data = pd.read_csv("dataset.csv")
    except FileNotFoundError:
        print("Error: dataset.csv not found.")
        return

    # Separate classes
    safe = data[data['label'] == 0]
    phish = data[data['label'] == 1]
    
    # UNDER-SAMPLING: Match the phishing count to the safe count (75 vs 75)
    # This prevents the model from just guessing 'Phishing' every time.
    min_size = min(len(safe), len(phish))
    df_balanced = pd.concat([
        safe.sample(n=min_size, random_state=42),
        phish.sample(n=min_size, random_state=42)
    ])
    
    print(f"Training on {len(df_balanced)} balanced samples ({min_size} Safe vs {min_size} Phish)...")

    # Step 2: Create the Pipeline
    # analyzer='char' is key: it looks for sequences like '.tk' or 'cbe-'
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4), max_features=2000)),
        ('rf', RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42))
    ])

    # Step 3: Split and Train
    X_train, X_test, y_train, y_test = train_test_split(
        df_balanced['url'], df_balanced['label'], test_size=0.2, random_state=42, stratify=df_balanced['label']
    )

    print("Step 4: Fitting Model...")
    model_pipeline.fit(X_train, y_train)

    # Step 5: Evaluation
    y_pred = model_pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nFinal Accuracy: {round(acc * 100, 2)}%")
    print("-" * 30)
    print(classification_report(y_test, y_pred, target_names=['Safe (0)', 'Phishing (1)']))

    # Step 6: Save for Render
    joblib.dump(model_pipeline, "model.pkl")
    print("-" * 30)
    print("SUCCESS: model.pkl is now ready for deployment!")

if __name__ == "__main__":
    train_phishguard_model()