# Generated by Django 5.2.1 on 2025-05-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_typeabonnement_duree'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonnement',
            name='date_fin',
            field=models.DateField(blank=True, null=True),
        ),
    ]
