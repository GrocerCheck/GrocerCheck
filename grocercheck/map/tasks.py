from __future__ import absolute_import, unicode_literals
from celery import task
from .current_scraper import run_scraper

@task(name="update_current_popularity", max_retries = 2, default_retry_delay = 10, time_limit = 1200)
def update_current_popularity(country, doBackup, doLog):
    run_scraper(country, doBackup, doLog)



@task(name="testruntask")
def TEST_TASK():
    open("/home/bitnami/apps/django/django_projects/GrocerCheck/temp.txt", "a+").write("oop\n")
