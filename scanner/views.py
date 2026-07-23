# Create your views here.
from django.shortcuts import render
from .AL.datasets.models.predict import predict_email

def home(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text")
        result = predict_email(text)

    return render(request, "scanner/home.html", {"result": result})

# where the magic happens, the predict_email function is called with the input text and returns the prediction result. This result is then passed to the template for rendering.