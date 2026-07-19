from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import pandas as pd

# Load dataset
df = pd.read_parquet("Testing.parquet")

# Features and labels
X = df.drop(columns=["status", "url"])
y = df["status"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LogisticRegression(max_iter=1000)

# Train model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Show a few predictions
for i in range(5):
    print("Actual:", y_test.iloc[i])
    print("Predicted:", predictions[i])
    print("-" * 30)

# Evaluate
print("Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Save model
joblib.dump(model, "url_model.pkl")

print("URL model saved successfully!")

