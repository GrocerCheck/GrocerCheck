from django.shortcuts import render

# Create your views here.



from map.models import Store
import json

def index(request):
    context = {}
    context['name'] = []
    context['lat'] = []
    context['lng'] = []
    context['place_id'] = []

    for s in Store.objects.all():        
        context['name'].append(s.name)
        context['lat'].append(s.lat)
        context['lng'].append(s.lng)
        context['place_id'].append(s.place_id)
        
            

    finalcontext = {}
    finalcontext['name'] = json.dumps(context['name'])
    finalcontext['lat'] = json.dumps(context['lat'])
    finalcontext['lng'] = json.dumps(context['lng'])
    finalcontext['place_id'] = json.dumps(context['place_id'])
    finalcontext['size'] = json.dumps([Store.objects.count()])

    


    return render(request,'index.html',context=finalcontext)
