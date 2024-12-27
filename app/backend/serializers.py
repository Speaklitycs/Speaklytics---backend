from rest_framework import serializers
from app.backend.models import ErrorModel

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorModel

class VideoUploadSerializer(serializers.Serializer):
    video = serializers.FileField()