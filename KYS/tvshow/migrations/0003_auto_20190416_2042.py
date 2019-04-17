# Generated by Django 2.1.2 on 2019-04-16 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvshow', '0002_remove_season_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tvshow.Season'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvshow.TVShow'),
        ),
    ]