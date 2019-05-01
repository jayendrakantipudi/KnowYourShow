from django.db import models
from cast.models import cast, director, producer
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class language(models.Model):
	languages = models.CharField(max_length=20)
	def __str__(self):
		return self.languages

class GENRE(models.Model):
	genres = models.CharField(max_length=25)
	def __str__(self):
		return self.genres


class review(models.Model):
	reviewer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
	show = models.ForeignKey('show', on_delete=models.SET_NULL,blank=True ,null=True)
	rating = models.IntegerField(null=True)
	Review = models.CharField(max_length=1000)
	edited = models.BooleanField(default=False)
	date_reviewed = models.DateField(blank=True, default=now)

class Show(models.Model):
	titleName = models.CharField(max_length=120)
	releaseDate = models.DateField()
	director = models.ManyToManyField(director)
	producer = models.ManyToManyField(producer)
	language = models.ManyToManyField(language)
	storyLine = models.CharField(max_length=2500)
	budget = models.FloatField(null=True)
	suggested_count = models.IntegerField(default=0)
	BoxOfficeCollection = models.FloatField(null=True)
	GENRE = models.ManyToManyField(GENRE)
	titlePoster = models.ImageField(upload_to='movie_posters',blank=True)
	cast = models.ManyToManyField(cast)
	movieViewCount = models.IntegerField(default= 0)
	def __str__(self):
		return self.titleName
