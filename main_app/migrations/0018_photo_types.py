# Generated by Django 4.0.4 on 2022-05-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_photo_party'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='types',
            field=models.CharField(choices=[('L', 'Lunar'), ('S', 'Solar'), ('C', 'Conjunction'), ('P', 'Planetary'), ('M', 'Meteor'), ('C', 'Comet'), ('AD', 'Asteroid'), ('AM', 'Astronomy'), ('SC', 'Spacraft')], default='L', max_length=2),
        ),
    ]
