from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('blog/', views.blog, name='blog'),
        path('sponsors/', views.sponsors, name='sponsors'),
        path('contact/', views.contact, name='contact'),
        path('media/', views.media, name='media'),
        ]
