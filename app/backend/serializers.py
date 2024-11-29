from rest_framework import serializers

class ErrorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    timestamp_start = serializers.FloatField()
    timestamp_end = serializers.FloatField()