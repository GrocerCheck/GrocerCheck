from __future__ import absolute_import, unicode_literals
from celery import task
from .current_scraper import run_scraper

@task(name="update_current_popularity")
def update_current_popularity(country, doBackup, doLog):
    run_scraper(country, doBackup, doLog)
