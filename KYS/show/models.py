from django.db import models

# Create your models here.

class language(models.Model):
	langs = (
			('Telugu','Telugu'),
			('Hindi','Hindi'),
			('English','English'),
			('Tamil','Tamil'),
			('Malyalam','Malyalam'),
		)
	languages = models.CharField(max_length=20, choices=langs)
	def __str__(self):
		return self.languages

class GENRE(models.Model):
	Genres = (
			('Horror','Horror'),
			('Thriller','Thriller'),
			('Comedy','Comedy'),
			('Adventure','Adventure'),
			('Action','Action'),
			('Fantasy','Fantasy'),
			('Romantic','Romantic'),
		)
	genres = models.CharField(max_length=20, choices=Genres)
	def __str__(self):
		return self.genres	


class show(models.Model):
	titleName = models.CharField(max_length=120)
	releaseDate = models.DateTimeField()
	languages = models.ManyToManyField(language)
	storyLine = models.CharField(max_length=1000)
	budget = models.FloatField(null=True)
	BoxOfficeCollection = models.FloatField(null=True)
	genre = models.ManyToManyField(GENRE)
	titlePoster = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.titleName

