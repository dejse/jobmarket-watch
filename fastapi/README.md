# FastAPI Job Market Dashboard

This is a FastAPI recreation of the Django job market dashboard, using raw SQL queries instead of an ORM.

## Project Structure

```
fastapi/
├── main.py                 # FastAPI application entry point
├── database.py             # Database connection and raw SQL queries
├── schemas.py              # Pydantic models for data validation
├── routes.py               # Route handlers for dashboard views
├── charts.py               # Plotly chart generation logic
├── import_csv.py           # CLI script for importing CSV data
├── templates/              # Jinja2 templates
│   ├── base.html          # Base template
│   ├── index.html         # Dashboard homepage
│   └── city_detail.html   # City detail page
├── static/                 # Static files (CSS, JS)
├── requirements.txt        # Python dependencies
└── db.sqlite3             # SQLite database (created on first run)
```

## Installation

1. Navigate to the fastapi directory:
```bash
cd fastapi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Import CSV Data

Before running the application, import the CSV data:

```bash
python import_csv.py --file ../data/data.csv
```

Options:
- `--file PATH`: Path to the CSV file (default: `../data/data.csv`)
- `--clear`: Clear existing data before importing

### 2. Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Or run the main.py file directly:

```bash
python main.py
```

The application will be available at:
- Dashboard: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### 3. Access the Dashboard

Open your browser and navigate to http://localhost:8000/ to view the dashboard.

## Features

- **Dashboard Overview**: View total jobs, cities tracked, and visualizations
- **Time Series Chart**: Track job counts over time for all cities
- **Bar Chart**: Current job counts by city
- **City Details**: Detailed statistics and trends for individual cities
- **Historical Data**: Complete data table for each city

## Key Differences from Django Version

1. **No ORM**: Uses raw SQL queries with `sqlite3` module
2. **Separate Database**: Uses its own `db.sqlite3` file
3. **FastAPI Framework**: Modern async framework with automatic API documentation
4. **Jinja2 Templates**: Similar to Django templates but with simpler URL routing
5. **Standalone Import Script**: Run directly with Python instead of Django management command

## Database Schema

The application uses a single table `job_data`:

```sql
CREATE TABLE job_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    location VARCHAR(100) NOT NULL,
    job_count INTEGER NOT NULL,
    UNIQUE(date, location)
);
```

With indexes on:
- `date`
- `location`
- `(date, location)` composite

## Development

The FastAPI application automatically initializes the database schema on startup using the `lifespan` event handler in `main.py`.

All database operations use context managers for safe connection handling and proper resource cleanup.
