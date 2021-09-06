from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Display the current Parsifal release"

    def handle(self, *args, **kwargs):
        self.stdout.write(settings.PARSIFAL_RELEASE)
