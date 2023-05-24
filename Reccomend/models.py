from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    movie_id=models.IntegerField(null=False)
    movie_title=models.CharField(max_length=100)
    movie_url=models.URLField(null=True)
    genre=models.CharField(max_length=100)
    def __str__(self):
        return str(self.movie_id)+" "+self.movie_title 

class Training(models.Model):
    user_id=models.IntegerField(null=False)
    movie_id=models.IntegerField(null=False)
    rating=models.DecimalField(max_digits=50, decimal_places=2)

class Questionnaire(models.Model):
    user_id  = models.IntegerField(null=False)
    weekends=models.CharField(max_length=100)
    weekdays=models.CharField(max_length=100)
    tired=models.CharField(max_length=100)
    happy=models.CharField(max_length=100)
    sad=models.CharField(max_length=100)
    inspiration=models.CharField(max_length=100)

class Playlist(models.Model):
    user_id = models.IntegerField(null=False)
    movie_id=models.IntegerField(null=False)