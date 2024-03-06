from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery_app import app as celery_app

from .models import GeneratedSubtitle
from .serializers import GenerateSubtitleSerializer, GenerateTranslationSerializer
from .tasks import generate_subtitle_task, generate_subtitle_translation_task


class GenerateSubtitleAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GenerateSubtitleSerializer(data=request.data)
        if serializer.is_valid():
            youtube_url = serializer.validated_data["youtube_url"]
            output_folder = "/tmp"

            # Enqueue the video processing task
            task = generate_subtitle_task.delay(youtube_url, output_folder)

            # Return the task ID to the client
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateTranslationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GenerateTranslationSerializer(data=request.data)
        if serializer.is_valid():
            source_content = serializer.validated_data["source"]

            task = generate_subtitle_translation_task.delay(source_content)

            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_task_status(request, task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    return JsonResponse({"status": task_result.status, "result": task_result.result}, status=status.HTTP_200_OK)


def get_subtitles(request, task_id):
    try:
        subtitle_record = GeneratedSubtitle.objects.get(task_id=task_id)
        return JsonResponse({"status": "success", "subtitles": subtitle_record.subtitles})
    except GeneratedSubtitle.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Subtitles not found"}, status=404)
