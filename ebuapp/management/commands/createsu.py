from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email='ccccc@naver.com').exists():
            User.objects.create_superuser(email='ccccc@naver.com', name='adminuser', password='passpass')