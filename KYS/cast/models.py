from django.db import models

# Create your models here.

class cast(models.Model):
	GENDER = (
			('Male','Male'),
			('Female','Female'),
			('Others','Others'),
		)
	name = models.CharField(max_length=120)
	age = models.IntegerField(null=True)
	gender = models.CharField(max_length=15, choices=GENDER)
	biography = models.CharField(max_length=1000)
	photo = models.ImageField(null=True, blank=True)
