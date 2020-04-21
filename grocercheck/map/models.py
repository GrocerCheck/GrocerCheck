from django.db import models

# Create your models here.



class Store(models.Model):
    ''' MODEL REPRESENTING A GROCERY STORE '''
    name = models.CharField(max_length=100)
    busyness = models.IntegerField()
    lat = models.CharField(max_length=10)
    lng = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    hours = models.CharField(max_length=10)
    placeID = models.CharField(max_length=100)

     
    def __str__(self):
        return self.name

	
