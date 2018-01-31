import sys
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Find ticker with increasing/decreasing volume patterns.'

    def add_arguments(self, parser):
        #parser.add_argument('-w', '--workers', type=int, default=1, help='number of workers.')
        parser.add_argument('-s', '--symbol', type=str, default="HPB", help='Specific symbol name')
        #parser.add_argument('--workers-timeout', type=int)

    def handle(self, *args, **options):
        symbol    = str(options['symbol'])
        print("Started with: %s" % symbol)

