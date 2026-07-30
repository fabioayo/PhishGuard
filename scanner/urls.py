from django.urls import path
from .views import home
from .api import AnalyzeAPIView

urlpatterns = [
    path("", home, name="home"),
    path("api/analyze/", AnalyzeAPIView.as_view(), name="analyze"),
]
