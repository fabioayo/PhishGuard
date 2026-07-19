import os
import joblib

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "email_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

def predict_email(email_text):
    email_vector=vectorizer.transform([email_text])
    return model.predict(email_vector)[0]
    # prediction=model.predict(email_vector)
    # return prediction[0]

# email=input("Enter an email:\n")

# result=predict_email(email)
# print ("\nPrediction:", result)