from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('covidwatch/', views.covidwatch, name='covidwatch'),
        path('sponsors/', views.sponsors, name='sponsors'),
        path('contact/', views.contact, name='contact'),
        path('media/', views.media, name='media'),
        path('covidwatch/<int:articleid>/', views.article, name='article'),
        ]
