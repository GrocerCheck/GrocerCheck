from __future__ import absolute_import, unicode_literals
from celery import task
from .current_scraper import run_scraper
from .current_scraper import run_proxy_scraper
from .current_scraper import threaded_scraper


@task(name="update_current_popularity", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def update_current_popularity(country, doBackup, doLog):
    run_scraper(country, doBackup, doLog)

@task(name="update_current_popularity_with_proxy", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def update_current_popularity_with_proxy(country, doBackup, doLog, proxy):
    run_scraper(country, doBackup, doLog, proxy)

@task(name="threaded_update_current_popularity")
def mp_update_current_popularity(country, doBackup, doLog, processes, max_retries = 2, default_retry_delay = 20, time_limit = 600):
    threaded_scraper(country, doBackup, doLog, numthreads)

@task(name="testruntask")
def TEST_TASK():
    open("/home/bitnami/apps/django/django_projects/GrocerCheck/temp.txt", "a+").write("oop\n")
