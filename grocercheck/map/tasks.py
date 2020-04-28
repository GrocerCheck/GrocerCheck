from __future__ import absolute_import, unicode_literals
from celery import task
import current_scraper

@task(name="update_current_popularity")
def update_current_popularity(country, doBackup, doLog):
    current_scraper.run_scraper(country, doBackup, doLog)
