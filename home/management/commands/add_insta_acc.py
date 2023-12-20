from django.core.management.base import BaseCommand
from home.models import instagram_accounts

class Command(BaseCommand):
    def add_arguments(self, parser):
            parser.add_argument('--id', 
                                help='After the run times, the bot will exit(0 means no effect)')
            parser.add_argument('--password', 
                                help='After the run times, the bot will exit(0 means no effect)')
    
    def handle(self, *args, **options):
        self.id = options.get('id')
        self.psd = options.get('password')
        instagram_accounts.objects.create(username=self.id,password=self.psd)