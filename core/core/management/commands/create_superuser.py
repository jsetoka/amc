# core/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
class Command(BaseCommand):
    help = 'Crée un superutilisateur automatiquement'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('Superutilisateur créé'))
        else:
            self.stdout.write('Superutilisateur existe déjà')
