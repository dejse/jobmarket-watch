"""CSV import script for job market data"""
import argparse
import pandas as pd
from pathlib import Path
import sys

from database import insert_many_job_data, clear_all_data, get_record_count, init_database


def main():
    """Import job market data from CSV file into the database"""
    parser = argparse.ArgumentParser(
        description='Import job market data from CSV file into the database'
    )
    parser.add_argument(
        '--file',
        type=str,
        default='../data/data.csv',
        help='Path to the CSV file (default: ../data/data.csv)'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing data before importing'
    )
    
    args = parser.parse_args()
    csv_file = args.file
    clear_data = args.clear
    
    print(f'Reading CSV file: {csv_file}')
    
    try:
        # Initialize database schema
        init_database()
        
        # Read CSV file using pandas
        df = pd.read_csv(csv_file)
        
        print(f'Found {len(df)} rows in CSV')
        
        # Clear existing data if requested
        if clear_data:
            count = get_record_count()
            deleted = clear_all_data()
            print(f'Deleted {deleted} existing records')
        
        # Prepare data for bulk insert
        records = []
        
        for _, row in df.iterrows():
            # Parse date
            date_val = pd.to_datetime(row['date']).date()
            location = row['location']
            job_count = int(row['job_count'])
            
            records.append((str(date_val), location, job_count))
        
        # Get initial count
        initial_count = get_record_count()
        
        # Bulk insert with ignore conflicts for duplicates
        inserted = insert_many_job_data(records)
        
        # Get final count to calculate actual inserts
        final_count = get_record_count()
        created_count = final_count - initial_count
        skipped = len(records) - created_count
        
        print(f'Successfully imported {created_count} records')
        
        if skipped > 0:
            print(f'Skipped {skipped} duplicate records')
        
        print(f'Total records in database: {final_count}')
        
    except FileNotFoundError:
        print(f'ERROR: CSV file not found: {csv_file}')
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: Error importing data: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
