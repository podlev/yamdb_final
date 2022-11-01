import csv

from django.core.management.base import BaseCommand

from reviews.models import Title, Categories


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/titles.csv", encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Categories.objects.get(pk=row['category'])
                )
