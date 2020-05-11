from __future__ import absolute_import, unicode_literals
from celery import task
from celery.signals import worker_process_init

from .current_scraper import run_scraper
from .hardcode_scrape import scrape
from multiprocessing import current_process
#attempted fix for config error w/ multiprocessing
#@worker_process_init.connect
#def fix_multiprocessing(**kwargs):
#    try:
#        current_process()._config
#    except AttributeError:
#        current_process()._config ={'semprefix':'/mp'}


@task(name="update_current_popularity", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def update_current_popularity(country, backup, log, prox, num_procs):
    run_scraper(country, doBackup = backup, doLog = log, proxy = prox, num_processes = num_procs)


@task(name="hardcoded_scrape", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def hardcoded_scrape():
    scrape()


@task(name="testruntask")
def TEST_TASK():
    open("/home/bitnami/apps/django/django_projects/GrocerCheck/temp.txt", "a+").write("oop\n")
