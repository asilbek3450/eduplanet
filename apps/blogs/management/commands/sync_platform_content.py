from django.core.management.base import BaseCommand

from site_content import ensure_platform_content


class Command(BaseCommand):
    help = 'Bootstrap EduPlanet bundled content; use --force to overwrite it.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Overwrite existing platform content with bundled demo content.',
        )

    def handle(self, *args, **options):
        changed = ensure_platform_content(force=options['force'])
        if changed:
            self.stdout.write(self.style.SUCCESS('Platform content bootstrapped.'))
        else:
            self.stdout.write('Existing platform content was kept.')
