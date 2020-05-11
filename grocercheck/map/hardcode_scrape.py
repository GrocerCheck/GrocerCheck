#!/usr/bin/python
from .current_scraper import run_scraper
import json

def scrape():
    print("whatthefuck")
    p = json.load(open("/home/bitnami/keys/luminati.txt"))
    try:
        run_scraper("Canada", proxy = p, num_processes = 8)
    except:
        print("something failed")


