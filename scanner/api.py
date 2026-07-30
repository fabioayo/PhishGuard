from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalysisSerializer
from .ml.services.analyzer import analyze_text


class AnalyzeAPIView(APIView):

    def get(self, request):
        return Response({
            "message": "Phishing Detector API is running"
        })

    def post(self, request):

        serializer = AnalysisSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        text = serializer.validated_data["text"]

        result = analyze_text(text)

        return Response(
            result,
            status=status.HTTP_200_OK
        )