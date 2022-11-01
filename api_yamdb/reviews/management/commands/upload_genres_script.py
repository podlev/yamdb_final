import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/genre.csv", encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            Genre.objects.bulk_create([
                Genre(
                    id=line['id'],
                    name=line['name'],
                    slug=line['slug']
                ) for line in reader
            ])
