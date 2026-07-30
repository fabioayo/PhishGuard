from scanner.ml.models.predict import predict_email
from scanner.ml.services.threat_engine import ThreatEngine
from scanner.ml.services.rules import check_rules
from scanner.ml.services.input_detector import InputDetector


def analyze_text(text):

    # Detect whether the input is an email, URL, or SMS
    detector = InputDetector()
    input_type = detector.detect(text)

    print(f"Detected input type: {input_type}")

    # Create a new threat engine for this analysis
    engine = ThreatEngine()

    # Run the ML model only for email input
    if input_type == "email":

        prediction = predict_email(text)

        if prediction["result"] == "Phishing":
            engine.add(
                60,
                "Machine Learning model classified the email as phishing."
            )

    else:

        prediction = {
            "result": "Safe",
            "confidence": 100
        }

    # Run all rule-based checks
    check_rules(text, engine)

    # Determine the final prediction
    if input_type == "email":

        final_prediction = prediction["result"]
        confidence = prediction["confidence"]

    elif input_type == "url":

        if engine.score >= 40:
            final_prediction = "Malicious URL"
        else:
            final_prediction = "Safe URL"

        confidence = 100

    else:

        if engine.score >= 40:
            final_prediction = "Suspicious SMS"
        else:
            final_prediction = "Safe SMS"

        confidence = 100

    # Build the final result
    result = engine.build_result(
        ml_prediction=final_prediction,
        ml_confidence=confidence
    )

    # Include the detected input type
    result["input_type"] = input_type

    return result