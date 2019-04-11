from django.db import models
from show.models import language, GENRE, review

# Create your models here.

class TVShow(models.Model):
    titleName = models.CharField(max_length=120)
    season = models.ManyToManyField(Season)
    seriesReview = models.ForeignKey(review, on_delete=models.SET_NULL,blank=True, null=True)
    GENRE = models.ManyToManyField(GENRE)
    language = models.ManyToManyField(language)
    seriesSummary = models.CharField(max_length=2500)
    seriesPoster = models.ImageField(upload_to='series_posters', blank=True)


class Season(models.Model):
    episode = models.ManyToManyField(Episode)
    seasonNum = models.IntegerField()


class Episode(models.Model):
    episodeNum = models.IntegerField()
    episodeName = models.CharField(max_length=50)
    releaseDate = models.DateField()
    cast = models.ManyToManyField(cast)
    episodeReview = models.ForeignKey(review, on_delete=models.SET_NULL, blank=True, null=True)
    runTime = models.DurationField()
    episodePoster = models.ImageField(upload_to='episode_posters', blank=True)
    cast = models.ManyToManyField(cast)
    episodeSummary = models.CharField(max_length=2500)