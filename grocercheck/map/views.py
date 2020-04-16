from django.shortcuts import render

# Create your views here.



from map.models import Store

def index(request):
	return render(request,'index.html')
