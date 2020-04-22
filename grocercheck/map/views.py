from django.shortcuts import render

# Create your views here.



from map.models import Store
import json

def index(request):
    context = {}
    context['name'] = []
    context['busyness'] = []
    context['lat'] = []
    context['lng'] = []
    context['address'] = []
    context['hours'] = []
    context['placeID'] = []

    for s in Store.objects.all():        
        context['name'].append(s.name)
        context['busyness'].append(s.busyness)
        context['lat'].append(s.lat)
        context['lng'].append(s.lng)
        context['address'].append(s.address)
        context['hours'].append(s.hours)
        context['placeID'].append(s.placeID)
        
            

    finalcontext = {}
    finalcontext['name'] = json.dumps(context['name'])
    finalcontext['busyness'] = json.dumps(context['busyness'])
    finalcontext['lat'] = json.dumps(context['lat'])
    finalcontext['lng'] = json.dumps(context['lng'])
    finalcontext['address'] = json.dumps(context['address'])
    finalcontext['hours'] = json.dumps(context['hours'])
    finalcontext['placeID'] = json.dumps(context['placeID'])
    finalcontext['size'] = json.dumps([Store.objects.count()])

    


    return render(request,'index.html',context=finalcontext)
