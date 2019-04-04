from django.db import models
from cast.models import cast
from django.contrib.auth.models import User

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
	reviewer = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	rating = models.IntegerField(null=True)
	Review = models.CharField(max_length=1000)

class Show(models.Model):
	titleName = models.CharField(max_length=120)
	releaseDate = models.DateTimeField()
	languages = models.ManyToManyField(language)
	storyLine = models.CharField(max_length=1000)
	budget = models.FloatField(null=True)
	BoxOfficeCollection = models.FloatField(null=True)
	genre = models.ManyToManyField(GENRE)
	titlePoster = models.ImageField(null=True, blank=True)
	actors = models.ManyToManyField(cast)
	Review = models.ForeignKey(review, on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.titleName
