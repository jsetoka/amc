# Generated by Django 5.2.1 on 2025-05-28 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_message_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='etat',
            field=models.CharField(choices=[('INIT', 'Initialisé'), ('PENDING', 'En cours'), ('DONE', 'Terminé')], max_length=20),
        ),
    ]
