from django.shortcuts import render
import time
import sqlite3
# Create your views here.
from django.conf import settings
import os

from map.models import Store
import json

def index(request):
    days = ['wed','tue','wed','thu','fri','sat','sun']
    day = days[time.localtime()[6]]
    hour = time.localtime()[3]
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
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR,'db1.sqlite3'))
    cur = conn.cursor()
    for s in Store.objects.all():
        with conn:
            context['name'].append(s.name)
            context['place_id'].append(s.place_id)
            context['address'].append(s.address)
            context['lat'].append(s.lat)
            context['lng'].append(s.lng)
            cur.execute('''SELECT '''+day+'''hours FROM map_store WHERE id=?''', (s.id,))
            context['hours'].append(cur.fetchone()[0])
            live = s.live_busyness
            if(live==None):
                cur.execute('''SELECT '''+day+hour+''' FROM map_store WHERE id=?''', (s.id,))
                live = cur.fetchone()[0]
                if(live==None):
                    live = -1
            else:
                live+=1000
            context['busyness'].append(live)



    finalcontext = {}

    for key in context.keys():
        finalcontext[key] = json.dumps(context[key])

    finalcontext['size'] = json.dumps([len(context['busyness'])])




    return render(request,'index.html',context=finalcontext)
