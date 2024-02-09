from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GenerateSubtitleSerializer
from .tasks import generate_subtitle_task


class GenerateSubtitleAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GenerateSubtitleSerializer(data=request.data)
        if serializer.is_valid():
            youtube_url = serializer.validated_data["youtube_url"]
            output_folder = "/tmp"

            # Enqueue the video processing task
            generate_subtitle_task.delay(youtube_url, output_folder)

            return Response({"message": "Video processing started successfully."}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
