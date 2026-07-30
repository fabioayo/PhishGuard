from rest_framework import serializers

class AnalysisSerializer(serializers.Serializer):
    text = serializers.CharField(
        required=True, allow_blank=False
    )