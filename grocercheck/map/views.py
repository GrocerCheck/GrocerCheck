from django.shortcuts import render

# Create your views here.



from map.models import Store
import json

def index(request):
    context = {}
    context["stores"] = json.dumps(['hi','test1','test2'])
    context["lat"] = json.dumps(['49.2399','49.2499','49.2399'])
    context['lon'] = json.dumps(['-123.1251','-123.1251','-123.1351'])
    return render(request,'index.html',context=context)
