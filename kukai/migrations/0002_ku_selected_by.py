# Generated by Django 3.1.2 on 2020-10-07 14:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kukai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ku',
            name='selected_by',
            field=models.ManyToManyField(blank=True, related_name='selector', to=settings.AUTH_USER_MODEL),
        ),
    ]
