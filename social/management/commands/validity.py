import datetime
from django.core.management.base import BaseCommand

from website.models import Token

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.now().date()
        print today
        q=Token.objects.filter(is_active=True)
        for data in q:
            validity=data.validity
            print validity
            if(today>validity):
                data.is_active=False
                data.save()
