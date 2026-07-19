# Create your views here.
from django.shortcuts import render
from .AL.datasets.models.predict import predict_email

def home(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text")
        result = predict_email(text)
        # print (result)

    return render(request, "scanner/home.html", {"result": result}) 