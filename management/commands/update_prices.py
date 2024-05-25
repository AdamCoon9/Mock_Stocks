from django.core.management.base import BaseCommand

from App1.tasks import update_stock_prices

 

class Command(BaseCommand):

    help = 'Updates the current value of all stocks'

 
def handle(self, *args, **options):

        update_stock_prices()