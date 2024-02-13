from django.db import models


class GeneratedSubtitle(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    subtitles = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
