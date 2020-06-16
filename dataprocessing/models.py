from django.db import models
import pickle
from django.core.validators import MaxValueValidator, MinValueValidator 
with open("Indiancitynames.txt", "rb") as fp:
    arr = pickle.load(fp)
class channel(models.Model):
    Channel_id = models.CharField(max_length=25)
    Channel_name = models.CharField(max_length=55)
    Channel_subscribers = models.IntegerField()
    Channel_views = models.IntegerField()
    Channel_query = models.CharField(max_length=100)
    Channel_city = models.CharField(max_length=100)
    Channel_video_count = models.IntegerField()
    class Meta:
        unique_together = ("Channel_id", "Channel_query" , "Channel_city",)

class userinput(models.Model):
    query = models.CharField(max_length=100)
    city = models.IntegerField(choices = arr) 
    number_queries = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(50)])
    def __str__(self): 
        return self.query 

