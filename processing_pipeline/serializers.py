from rest_framework import serializers


class GenerateSubtitleSerializer(serializers.Serializer):
    youtube_url = serializers.URLField()
