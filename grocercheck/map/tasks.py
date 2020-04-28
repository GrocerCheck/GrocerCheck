from __future__ import absolute_import, unicode_literals
from celery import task

@shared_task(name='taskone')
def taskone(string):
    print(string)

