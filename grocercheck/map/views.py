from django.shortcuts import render
import time
import sqlite3
from django.conf import settings
import os
import datetime
import pytz
from map.models import Store
import json


def index(request, city="nocity"):
    city2tz = {'vancouver': 'America/Vancouver', 'los_angeles':  'America/Vancouver', 'silicon_valley': 'America/Vancouver',
                'portland': 'America/Vancouver', 'seattle': 'America/Vancouver',
               'new_york': 'America/Toronto', 'toronto': 'America/Toronto', 'victoria': 'America/Vancouver', 'las_vegas': 'America/Vancouver'}
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
    if(popupflag):
        context['popupflag'].append("yes")
    else:
        context['popupflag'].append("no")
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR,'db1.sqlite3'))
    cur = conn.cursor()
    for s in Store.objects.filter(city__exact=city):
        with conn:
            context['name'].append(s.name)
            context['place_id'].append(s.place_id)
            context['address'].append(s.address)
            context['lat'].append(s.lat)
            context['lng'].append(s.lng)
            cur.execute('''SELECT '''+day+'''hours FROM map_store WHERE id=?''', (s.id,))
            hourstring = cur.fetchone()[0]
            context['hours'].append(hourstring)
            if(s.keywords==None):
                context['keywords'].append("")

            else:
                context['keywords'].append(s.keywords)

            live = s.live_busyness
            if(live==None):
                cur.execute('''SELECT '''+day+hour+''' FROM map_store WHERE id=?''', (s.id,))
                live = cur.fetchone()[0]
                if(live==None):
                    live = -1
            else:
                live+=1000
            context['busyness'].append(live)
            #Monday: 7:00 AM – 10:00 PM
            if(hourstring==None):
                context['openn'].append(0)
            else:
                hours = hourstring.split(": ")[1]
                if (' 24' in hours):
                    context['openn'].append(1)
                elif ('–' not in hours):
                    context['openn'].append(0)
                else:
                    hours = hours.split(" – ")
                    oh, om = int(hours[0].split(':')[0]), int(hours[0].split(':')[1][:2]) #opening hour, opening minute
                    ch, cm = int(hours[1].split(':')[0]), int(hours[1].split(':')[1][:2]) #closing hour, closing minute

                    if ((hours[0][-2:] == "PM") and (oh != 12)):
                        oh += 12
                    if ((hours[1][-2:] == "PM") and (ch !=12)): #12PM is noon, 12AM is midnight
                        ch += 12
                    if ((hours[0][-2:] == "AM") and (oh == 12)):
                        oh = 0 #if it opens at midnight, set to 0 for comparison
                    if ((hours[1][-2:] == "AM") and (ch == 12)):
                        ch = 24

                    if ((hours[1][-2:] == "AM") and (ch < oh)) or ((hours[1][-2:] == "AM") and (ch == 24)): #check if the store closes after midnight or at midnight
                        if (ch == 24):
                            if ((localhour < ch) and (localhour > oh)):
                                context['openn'].append(1)
                            else:
                                context['openn'].append(0)
                        else:
                            if (localhour >= oh):
                                context['openn'].append(1)
                            if (localhour < ch):
                                context['openn'].append(1)

                            elif (localhour == ch and localminute < cm):
                                context['openn'].append(1)
                    else:
                            if(localhour>oh and localhour<ch):
                                context['openn'].append(1)
                            elif(localhour==oh and localminute>=om):
                                context['openn'].append(1)
                            elif(localhour==ch and localminute<cm):
                                context['openn'].append(1)
                            else:
                                context['openn'].append(0)




    finalcontext = {}

    for key in context.keys():
        finalcontext[key] = json.dumps(context[key])

    finalcontext['size'] = json.dumps([len(context['busyness'])])




    return render(request,'index.html',context=finalcontext)

def about(request):
    return render(request,'about.html')

def covidwatch(request):
    return render(request, 'covidwatch.html')

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
        curr.execute("SELECT id,title,author_name,author_blurb,date,content,image_blurb,article_sources FROM map_blog_entry WHERE id=?", (articleid,))
        art = curr.fetchall()[0]
        context['title'] = json.dumps(art[1], ensure_ascii=False)
        context['author_name'] = json.dumps(art[2], ensure_ascii=False)
        context['author_blurb'] = json.dumps(art[3], ensure_ascii=False)
        context['date'] = json.dumps(art[4], ensure_ascii=False)
        context['content'] = json.dumps(art[5], ensure_ascii=False)
        context['image_blurb'] = json.dumps(art[6], ensure_ascii=False)
        context['article_sources'] = json.dumps(art[7], ensure_ascii=False)


    return render(request, 'article.html', context=context)

