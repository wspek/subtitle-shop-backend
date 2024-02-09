from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import GenerateSubtitleAPIView

urlpatterns = [
    path("get-subtitle/", csrf_exempt(GenerateSubtitleAPIView.as_view()), name="get-subtitle"),
]
