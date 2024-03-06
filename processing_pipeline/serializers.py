from rest_framework import serializers


class GenerateSubtitleSerializer(serializers.Serializer):
    youtube_url = serializers.URLField()


class GenerateTranslationSerializer(serializers.Serializer):
    source = serializers.CharField()
