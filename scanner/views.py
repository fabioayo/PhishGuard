from django.shortcuts import render
from .ml.models.predict import predict_email
from .ml.services.threat_engine import ThreatEngine


def home(request):

    result = None

    if request.method == "POST":

        text = request.POST.get("text")

        prediction = predict_email(text)

        engine = ThreatEngine()

        # Machine Learning Result
        if prediction["result"] == "Phishing":
            engine.add(
                60,
                "Machine Learning model classified the email as phishing."
            )

        # Rule-Based Checks
        if "urgent" in text.lower():
            engine.add(
                10,
                "Urgency language detected."
            )

        if "password" in text.lower():
            engine.add(
                20,
                "Sensitive credential request detected."
            )

        if "click here" in text.lower():
            engine.add(
                10,
                "Suspicious call-to-action detected."
            )
        result = engine.build_result(
            ml_prediction=prediction["result"],
            ml_confidence=prediction["confidence"]
            )
    
    return render(request, "scanner/home.html", {"result": result})