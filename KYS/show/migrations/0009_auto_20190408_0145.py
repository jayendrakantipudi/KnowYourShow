# Generated by Django 2.1.3 on 2019-04-07 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0008_auto_20190407_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='director',
            field=models.CharField(default=None, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='producer',
            field=models.CharField(default=None, max_length=120),
            preserve_default=False,
        ),
    ]