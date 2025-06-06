import csv
from django.core.management.base import BaseCommand
from Analysis.models import Candidate


class Command(BaseCommand):
    help = 'Import data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Candidate.objects.create(
                    user_id=row['id'],
                    city=row['city'],
                    state=row['state'],
                    country=row['country'],
                    keywords=row['KeyWords'],
                    awards=row['awards'],
                    education=row['Education'],
                    graduation_date=row['Graduation_Date'],
                    job_title=row['job_Title'],
                    previous_organization=row['Previous_organization'],
                    certifications=row['certifications']

                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
