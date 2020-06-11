from django.shortcuts import render
from django.conf import settings
import time
import sqlite3
import datetime
import pytz
import json
import os
from os.path import expanduser
import random

from map.models import Store
from map.models import blog_entry

def index(request, city="nocity"):
    city2tz = {'vancouver': 'America/Vancouver', 'los_angeles':  'America/Vancouver',
               'silicon_valley': 'America/Vancouver', 'portland': 'America/Vancouver',
               'seattle': 'America/Vancouver', 'montreal': 'America/Montreal',
               'new_york': 'America/Toronto', 'toronto': 'America/Toronto',
               'victoria': 'America/Vancouver', 'las_vegas': 'America/Vancouver',


               }
    popupflag = False
    if(city=="nocity"):
        popupflag = True
        city = "vancouver"


    timezone = pytz.timezone(city2tz[city])
    days = ['mon','tue','wed','thu','fri','sat','sun']

    t = datetime.datetime.now(timezone)
    day = days[t.weekday()]
    hour = t.hour
    localhour = t.hour
    localminute = t.minute

    if(hour<10):
        hour = '0'+str(hour)
    else:
        hour = str(hour)
    context = {}
    context['name'] = []
    context['place_id'] = []
    context['address'] = []
    context['lat'] = []
    context['lng'] = []
    context['hours'] = []
    context['busyness'] = []
    context['openn'] = []
    context['keywords'] = []
    context['popupflag'] = []
    context['city'] = []
    context['city'].append(city)

    if(popupflag):
        context['popupflag'].append("yes")
    else:
        context['popupflag'].append("no")
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR,'db1.sqlite3'))
    cur = conn.cursor()
    with conn:
# I suppose we could be using models for this...
        cur.execute("SELECT * FROM map_ad_placement WHERE ad_blurb != '__NO-SHOW__' AND ad_city LIKE "+chr(39)+chr(37)+city+chr(37)+chr(39))
        ads = cur.fetchall()
        if len(ads) == 0:
            # context['blurbs'] = datetime.datetime.now(timezone).strftime("%m/%d/%Y, %H:%M:%S")
            context['blurbs'] = "This could be you! Contact us to advertise with GrocerCheck"
            context['links'] = "mailto:preston@grocercheck.ca?subject=GrocerCheck Advertising Inquiry"
            context['images'] = "http://drive.google.com/uc?id=1VgMaQckiTGqvmM9MzoBhhjb65SNsr_LF"
        else:
            ad = random.choice(ads)
            context['blurbs'] = ad[1]
            context['images'] = ad[2]
            context['links'] = ad[3]
    cur = conn.cursor()

    for s in Store.objects.filter(city__exact=city):
        with conn:
            context['name'].append(s.name)
            context['place_id'].append(s.place_id)
            context['address'].append(s.address)
            context['lat'].append(s.lat)
            context['lng'].append(s.lng)
            cur.execute("SELECT "+day+"hours FROM map_store WHERE id=?", (s.id,))
            hourstring = cur.fetchone()[0]
            context['hours'].append(hourstring)
            if(s.keywords==None):
                context['keywords'].append("")
            else:
                context['keywords'].append(s.keywords)

            live = s.live_busyness
            if(live==None):
                cur.execute("SELECT "+day+hour+" FROM map_store WHERE id=?", (s.id,))
                live = cur.fetchone()[0]
                if(live==None):
                    live = -1
            else:
                live+=1000
            context['busyness'].append(live)

            if(hourstring==None):
                context['openn'].append(0)
            else:
                hours = hourstring.split(": ")[1]#Friday: 8:00 AM - 7:00 PM
                #8:00 AM - 7:00 PM
                if (' 24' in hours):
                    context['openn'].append(1)
                elif ('–' not in hours):
                    context['openn'].append(0)
                else:
                    hours = hours.split(" – ")#[8:00 AM,7:00 PM]
                    ostring = hours[0].split(':')#[8,00 AM]
                    cstring = hours[1].split(':')#[7,00 PM]

                    oh, om, omod = int(ostring[0]), int(ostring[1][:2]), ostring[1][-2:] #opening hour, opening minute, opening modifier
                    ch, cm, cmod = int(cstring[0]), int(cstring[1][:2]), cstring[1][-2:] #closing hour, closing minute, closing modifier

                    if omod=='AM' and oh==12:
                        oh = 0
                    if omod=='PM' and oh!=12:
                        oh+=12
                    if cmod=='PM' and ch!=12:
                        ch+=12
                    if cmod=='AM' and ch==12:
                        ch==24
                    if cmod=='AM' and omod=='AM' and ch<oh and ch!=12:
                        ch+=24
                    if cmod=='AM' and omod=='PM':
                        ch+=24
                    if localhour>oh and localhour<ch:
                        context['openn'].append(1)
                    elif localhour==oh and localminute>=om:
                        context['openn'].append(1)
                    elif localhour==ch and localminute<ch:
                        context['openn'].append(1)
                    else:
                        context['openn'].append(0)



    finalcontext = {}

    for key in context.keys():
        finalcontext[key] = json.dumps(context[key])


    finalcontext['size'] = json.dumps([len(context['busyness'])])


    try:
        finalcontext['apikey'] = open("/home/bitnami/keys/gmapjs.txt").readline().strip()
    except:
        finalcontext['apikey'] = open(expanduser('~')+"/keys/gmapjs.txt").readline().strip()

    return render(request,'index.html',context=finalcontext)

def about(request):
    return render(request,'about.html')

def covidwatch(request):
    # return render(request, 'covidwatch.html')
    context = {}
    context['blog_entries'] = []
    for entry in blog_entry.objects.all():
        if entry.title=="__NO-SHOW__":
            continue
        else:
            blog_entries = {}
            blog_entries['id'] = entry.id
            blog_entries['title'] = entry.title
            blog_entries['author_name'] = entry.author_name
            blog_entries['first_line'] = entry.content.split('.')[0]+'.'
            blog_entries['img_src'] = entry.img_src
            blog_entries['img_blurb'] = entry.image_blurb
            context['blog_entries'].append(blog_entries)

    # finalcontext = {}
    # for key in context.keys():
    #     finalcontext[key] = json.dumps(context[key])

    # context['lrange'] = list(range(len(context['id'])))
    # context['urange'] = list(range(1, (len(context['id'])+1)))

    return render(request, 'dynamicCovidWatch.html', context=context)


def partners(request):
    return render(request, 'sponsors.html')

def contact(request):
    return render(request, 'contact.html')

def media(request):
    return render(request, 'media.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def cookies(request):
    return render(request, 'cookies.html')


def article(request, articleid):
    #id, title, author_name, author_blurb, date, content
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR,'db1.sqlite3'))
    curr = conn.cursor()
    context = {}
    with conn:
        curr.execute("SELECT id,title,author_name,author_blurb,date,content,image_blurb,article_sources,img_src FROM map_blog_entry WHERE id=?", (articleid,))
        art = curr.fetchall()[0]
        context['title'] = json.dumps(art[1], ensure_ascii=False)
        context['author_name'] = json.dumps(art[2], ensure_ascii=False)
        context['author_blurb'] = json.dumps(art[3], ensure_ascii=False)
        context['date'] = json.dumps(art[4], ensure_ascii=False)
        context['content'] = json.dumps(art[5], ensure_ascii=False)
        context['image_blurb'] = json.dumps(art[6], ensure_ascii=False)
        context['article_sources'] = json.dumps(art[7], ensure_ascii=False)
        context['img_src'] = json.dumps(art[8], ensure_ascii=False)
    return render(request, 'article.html', context=context)

