import csv

from django.core.management.base import BaseCommand

from reviews.models import Categories


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/category.csv", encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            Categories.objects.bulk_create([
                Categories(
                    id=line['id'],
                    name=line['name'],
                    slug=line['slug']
                ) for line in reader
            ])
