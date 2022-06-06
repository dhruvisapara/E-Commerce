import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "E_Commrce.settings")
app = Celery("E_Commrce")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
