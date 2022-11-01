import csv

from django.core.management.base import BaseCommand

from reviews.models import GenreTitle, Title, Genre


class Command(BaseCommand):
    def handle(self, **options):
        with open("static/data/genre_title.csv", encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    title_id=Title.objects.get(id=row['title_id']),
                    genre_id=Genre.objects.get(id=row['genre_id'])
                )
