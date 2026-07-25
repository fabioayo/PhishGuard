from django.shortcuts import render
from .ml.models.predict import predict_email
from .ml.services.threat_engine import ThreatEngine
from .ml.services.rules import check_rules


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
        check_rules(text, engine)
        
        result = engine.build_result(
            ml_prediction=prediction["result"],
            ml_confidence=prediction["confidence"]
            )
    
    return render(request, "scanner/home.html", {"result": result})