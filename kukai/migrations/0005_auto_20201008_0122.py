# Generated by Django 3.1.2 on 2020-10-07 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kukai', '0004_unza_participants'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unza',
            old_name='participants',
            new_name='selectors',
        ),
    ]
