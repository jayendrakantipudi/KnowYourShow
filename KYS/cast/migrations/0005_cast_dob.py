# Generated by Django 2.1.3 on 2019-04-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cast', '0004_auto_20190409_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='cast',
            name='dob',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]