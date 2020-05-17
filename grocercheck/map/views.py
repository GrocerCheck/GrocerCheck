from django.shortcuts import render
import time
import sqlite3
# Create your views here.
from django.conf import settings
import os

from map.models import Store
import json



def index(request, city="vancouver"):
    days = ['mon','tue','wed','thu','fri','sat','sun']
    t = time.localtime()
    day = days[t[6]]
    hour = t[3]
    rawhour = t[3]
    minute = t[4]

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
                spl = hourstring.split(": ")[1]
                if ('24' in spl):
                    context['openn'].append(1)
                elif ('–' not in spl):
                    context['openn'].append(0)
                else:
                    spl = spl.split(' – ')
                    o, c = spl[0],spl[1]
                    oh = int(o.split(':')[0])
                    om = int(o.split(':')[1][:2])
                    ch = int(c.split(':')[0])
                    cm = int(c.split(':')[1][:2])
                    if(o[-2:]=='PM'):
                        oh+=12
                    if(c[-2:]=='PM'):
                        ch+=12
                    if(rawhour>oh and rawhour<ch):
                        context['openn'].append(1)
                    elif(rawhour==oh and minute>=om):
                        context['openn'].append(1)
                    elif(rawhour==ch and minute<cm):
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

def sponsors(request):
    return render(request, 'sponsors.html')

def contact(request):
    return render(request, 'contact.html')

def media(request):
    return render(request, 'media.html')

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

