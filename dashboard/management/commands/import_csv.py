import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from dashboard.models import JobData
from datetime import datetime


class Command(BaseCommand):
    help = 'Import job market data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/data.csv',
            help='Path to the CSV file (default: data/data.csv)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing'
        )

    def handle(self, *args, **options):
        csv_file = options['file']
        clear_data = options['clear']

        self.stdout.write(f'Reading CSV file: {csv_file}')

        try:
            # Read CSV file using pandas
            df = pd.read_csv(csv_file)
            
            self.stdout.write(f'Found {len(df)} rows in CSV')

            # Clear existing data if requested
            if clear_data:
                count = JobData.objects.count()
                JobData.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {count} existing records')
                )

            # Prepare data for bulk insert
            job_data_objects = []
            skipped = 0
            
            for _, row in df.iterrows():
                # Parse date
                date = pd.to_datetime(row['date']).date()
                location = row['location']
                job_count = int(row['job_count'])
                
                job_data_objects.append(
                    JobData(
                        date=date,
                        location=location,
                        job_count=job_count
                    )
                )

            # Bulk create with ignore_conflicts to skip duplicates
            try:
                created = JobData.objects.bulk_create(
                    job_data_objects,
                    ignore_conflicts=True
                )
                created_count = len(created)
            except Exception as e:
                # Fallback: insert one by one
                self.stdout.write(
                    self.style.WARNING('Bulk insert failed, trying individual inserts')
                )
                created_count = 0
                skipped = 0
                for obj in job_data_objects:
                    try:
                        obj.save()
                        created_count += 1
                    except Exception:
                        skipped += 1
                        
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully imported {created_count} records'
                    )
                )
                if skipped > 0:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipped {skipped} duplicate records'
                        )
                    )
                return
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported {created_count} records'
                )
            )
            
            if created_count < len(job_data_objects):
                skipped = len(job_data_objects) - created_count
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped {skipped} duplicate records'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing data: {str(e)}')
            )
