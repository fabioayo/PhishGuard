from django.shortcuts import render
from .ml.models.predict import predict_email
from .ml.services.threat_engine import ThreatEngine
from .ml.services.rules import check_rules
from scanner.ml.services.input_detector import InputDetector


def home(request):

    result = None

    if request.method == "POST":

        text = request.POST.get("text")
        
        detector = InputDetector()
        input_type = detector.detect(text)
        
        print(f"Detected input type: {input_type}")

        engine = ThreatEngine()
        
        # Machine Learning Result
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

        # Rule-Based Checks
        check_rules(text, engine)
        
        if input_type == "email":
            ml_prediction = prediction["result"]
            ml_confidence = prediction["confidence"]
            
        elif input_type == "url":
            
            if engine.score >= 40:
                ml_prediction = "Malicious URL"
            else:
                ml_prediction = "Safe URL"
                
            ml_confidence = 100
            
        else:
            if engine.score >= 40:
                ml_prediction = "Suspicious SMS"
            else:
                ml_prediction = "Safe SMS"
                
            ml_confidence = 100
            
        result = engine.build_result(
            ml_prediction=ml_prediction,
            ml_confidence=ml_confidence
            )
    
    return render(request, "scanner/home.html", {"result": result})