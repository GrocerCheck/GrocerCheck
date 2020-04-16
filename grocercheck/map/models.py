from django.db import models

# Create your models here.



class Store(models.Model):
	''' MODEL REPRESENTING A GROCERY STORE '''
	name = models.CharField(max_length=100)
	busyness = models.IntegerField()

	def __str__(self):
		return self.name

	
