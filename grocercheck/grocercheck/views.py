from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
import os



def submit_view(request):
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfD3L5Dif_8Gq3gqVxrErTESX8Kn6hfMyuweYfcWPjYphy3Rw/viewform")

