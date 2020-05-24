from __future__ import absolute_import, unicode_literals
from celery import task
from celery.signals import worker_process_init

from .current_scraper import run_scraper
from .hardcode_scrape import scrape
from .updateDBscripts import *

#from multiprocessing import current_process
#attempted fix for config error w/ multiprocessing
#@worker_process_init.connect
#def fix_multiprocessing(**kwargs):
#    try:
#        current_process()._config
#    except AttributeError:
#        current_process()._config ={'semprefix':'/mp'}


@task(name="upload_lpt", max_retries=3, default_retry_delay = 10, time_limit = 60)
def upload_lpt(remote_conn, local_conn):
    updateRemoteDump(remote_conn, local_conn)

@task(name="download_lpt", max_retries=3, default_retry_delay = 10, time_limit = 60)
def upload_lpt(remote_conn, local_conn):
    updateLocal(remote_conn, local_conn)

@task(name="update_map_rows", max_retries=2, default_retry_delay = 20, time_limit = 1000)
def update_map_rows(remote_conn, local_conn):
    updateMapStore(remote_conn, local_conn)

@task(name="update_blog_rows", max_retries=2, default_retry_delay = 20, time_limit = 1000)
def update_map_rows(remote_conn, local_conn):
    updateBlogStore(remote_conn, local_conn)

@task(name="log_lpt", max_retries = 2, default_retry_delay = 10, time_limit = 20)
def log_lpt(remote_conn):
    updateBackup(remote_conn)



@task(name="update_current_popularity", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def update_current_popularity(country, city, backup, log, prox, num_procs):
    run_scraper(country, city, doBackup = backup, doLog = log, proxy = prox, num_processes = num_procs)


@task(name="hardcoded_scrape", max_retries = 2, default_retry_delay = 20, time_limit = 420)
def hardcoded_scrape():
    scrape()


@task(name="testruntask")
def TEST_TASK():
    open("/home/bitnami/apps/django/django_projects/GrocerCheck/temp.txt", "a+").write("oop\n")
