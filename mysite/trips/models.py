from django.db import models

# Create your models here.
class Post(models.Model):
	shop = models.CharField(max_length=100)
	place = models.CharField(max_length=100)
	longitude = models.FloatField()
	latitude = models.FloatField()
	
	def __str__(self):
		return self.shop