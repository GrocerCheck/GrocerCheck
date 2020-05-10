from __future__ import absolute_import, unicode_literals
from celery import task
from current_scraper import run_scraper
from hardcode_scrape import scrape



@task(name="update_current_popularity", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def update_current_popularity(country, backup, log, prox, num_procs):
    run_scraper(country, doBackup = backup, doLog = log, proxy = prox, num_processes = num_procs)


@task(name="hardcoded_scrape", max_retries = 2, default_retry_delay = 20, time_limit = 420):
def hardcoded_scrape():
    scrape()


@task(name="testruntask")
def TEST_TASK():
    open("/home/bitnami/apps/django/django_projects/GrocerCheck/temp.txt", "a+").write("oop\n")
