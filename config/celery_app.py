import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("subtitle_shop_backend")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Use RabbitMQ as the broker
app.conf.broker_url = "amqp://subtitle-shop:hurlingham@localhost/subtitle-shop"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
