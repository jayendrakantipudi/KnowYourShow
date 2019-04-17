# Generated by Django 2.1.2 on 2019-04-16 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('show', '__first__'),
        ('cast', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episodeNum', models.IntegerField()),
                ('episodeName', models.CharField(max_length=50, null=True)),
                ('releaseDate', models.DateField()),
                ('runTime', models.DurationField()),
                ('episodePoster', models.ImageField(blank=True, upload_to='series_posters/episode_posters')),
                ('episodeSummary', models.CharField(max_length=2500)),
                ('cast', models.ManyToManyField(to='cast.cast')),
                ('episodeReview', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='show.review')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seasonNum', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleName', models.CharField(max_length=120)),
                ('seriesSummary', models.CharField(max_length=2500)),
                ('seriesPoster', models.ImageField(blank=True, upload_to='series_posters')),
                ('GENRE', models.ManyToManyField(to='show.GENRE')),
                ('language', models.ManyToManyField(to='show.language')),
                ('seriesReview', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='show.review')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tvshow.TVShow'),
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tvshow.Season'),
        ),
        migrations.AddField(
            model_name='episode',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tvshow.TVShow'),
        ),
    ]