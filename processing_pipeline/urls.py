from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import GenerateSubtitleAPIView, get_subtitles, get_task_status

urlpatterns = [
    path("get-subtitle/", csrf_exempt(GenerateSubtitleAPIView.as_view()), name="get-subtitle"),
    path("tasks/status/<str:task_id>/", get_task_status, name="task_status"),
    path("subtitles/<str:task_id>/", get_subtitles, name="get_subtitles"),
]
