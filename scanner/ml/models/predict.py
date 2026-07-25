import os
import joblib

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "email_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))


def predict_email(email_text):

    email_vector = vectorizer.transform([email_text])

    # Predict class
    prediction = model.predict(email_vector)[0]

    # Predict probabilities
    probabilities = model.predict_proba(email_vector)[0]

    # Highest confidence
    confidence = float(round(max(probabilities) * 100,2))

    return {
        "result": prediction,
        "confidence": confidence
    }