from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Project4_App_level.views import update_portfolio  # Import the update_portfolio function

class Command(BaseCommand):
    help = 'Updates the portfolio for each user'

    def handle(self, *args, **options):
        # Get all users
        users = User.objects.all()

        # Update the portfolio for each user
        for user in users:
            update_portfolio(user)
