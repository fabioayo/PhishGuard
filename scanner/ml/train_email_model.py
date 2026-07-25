from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import pandas as pd

#Train Email model

# Load dataset
df = pd.read_csv("Phishing_Email.csv")

# Remove rows with missing email text
df = df.dropna(subset=["Email Text"])

# Features and labels
X = df["Email Text"]
y = df["Email Type"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# print(X_train.shape)
# print(X_test.shape)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

for i in range(5):
    print("Actual:", y_test.iloc[i])
    print("Predicted:", predictions[i])
    print("-" * 30)

print("Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

joblib.dump(model, "models/email_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model saved successfully!")
