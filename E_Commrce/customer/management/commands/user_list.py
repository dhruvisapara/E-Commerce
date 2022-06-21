from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
from customer.models import Customer


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            Customer.objects.create_user(username=get_random_string(), email='', password='123')
