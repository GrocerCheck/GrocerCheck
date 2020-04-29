from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grocercheck.settings")

app = Celery('grocercheck')
#namespace="Celery" means that all celery config keys should have a "CELERY_" prefix
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_test(self):
    print("Request: {0!r}",format(self.request))


