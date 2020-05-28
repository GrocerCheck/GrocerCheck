from django.urls import path
from . import views

urlpatterns = [


        path('about/', views.about, name='about'),
        path('covidwatch/<int:articleid>/', views.article),
        path('covidwatch/', views.covidwatch, name='covidwatch'),
        path('partners/', views.partners, name='partners'),
        path('contact/', views.contact, name='contact'),
        path('media/', views.media, name='media'),
        path('terms/', views.terms, name='terms'),
        path('privacy/', views.privacy, name='privacy'),
        path('cookies/', views.cookies, name='cookies'),
        path('<str:city>/', views.index),
        path('', views.index, name='index'),
        
                ]
