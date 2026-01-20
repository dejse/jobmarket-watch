"""Database connection and raw SQL queries for job market data"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import date

# Database file path
DB_PATH = Path(__file__).parent / "db.sqlite3"


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Enable accessing columns by name
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """Initialize database schema with tables and indexes"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create job_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                location VARCHAR(100) NOT NULL,
                job_count INTEGER NOT NULL,
                UNIQUE(date, location)
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date ON job_data(date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_location ON job_data(location)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date_location ON job_data(date, location)
        """)
        
        conn.commit()


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert sqlite3.Row to dictionary"""
    return dict(row)


def get_latest_date() -> Optional[str]:
    """Get the latest date in the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT MAX(date) as max_date FROM job_data").fetchone()
        return result['max_date'] if result else None


def get_latest_data() -> List[Dict[str, Any]]:
    """Get all data for the latest date, ordered by job_count descending"""
    latest_date = get_latest_date()
    if not latest_date:
        return []
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        results = cursor.execute(
            """
            SELECT id, date, location, job_count 
            FROM job_data 
            WHERE date = ? 
            ORDER BY job_count DESC
            """,
            (latest_date,)
        ).fetchall()
        
        return [row_to_dict(row) for row in results]


def get_all_data() -> List[Dict[str, Any]]:
    """Get all data ordered by date and location"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        results = cursor.execute(
            """
            SELECT id, date, location, job_count 
            FROM job_data 
            ORDER BY date, location
            """
        ).fetchall()
        
        return [row_to_dict(row) for row in results]


def get_city_data(location: str) -> List[Dict[str, Any]]:
    """Get all data for a specific city, ordered by date"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        results = cursor.execute(
            """
            SELECT id, date, location, job_count 
            FROM job_data 
            WHERE location = ? 
            ORDER BY date
            """,
            (location,)
        ).fetchall()
        
        return [row_to_dict(row) for row in results]


def insert_job_data(date_val: str, location: str, job_count: int) -> bool:
    """Insert a single job data record, ignore if duplicate"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO job_data (date, location, job_count) 
                VALUES (?, ?, ?)
                """,
                (date_val, location, job_count)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False


def insert_many_job_data(records: List[tuple]) -> int:
    """
    Bulk insert job data records, ignore duplicates
    
    Args:
        records: List of tuples (date, location, job_count)
    
    Returns:
        Number of records inserted
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany(
                """
                INSERT OR IGNORE INTO job_data (date, location, job_count) 
                VALUES (?, ?, ?)
                """,
                records
            )
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error bulk inserting data: {e}")
            return 0


def clear_all_data() -> int:
    """Delete all data from job_data table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job_data")
        conn.commit()
        return cursor.rowcount


def get_record_count() -> int:
    """Get total number of records in the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT COUNT(*) as count FROM job_data").fetchone()
        return result['count'] if result else 0
