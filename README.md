# Job Market Watch Austria

A Django web application that tracks and visualizes job market data for Controller positions across Austrian cities, scraped from Karriere.at.

## Features

- 📊 Interactive dashboard with Plotly visualizations
- 📈 Historical trend analysis for job counts
- 🏙️ City-specific detailed views
- 🔄 Automated data scraping via GitHub Actions
- 💾 SQLite database for persistent storage
- 🎨 Modern, responsive UI

## Setup

### Prerequisites

- Python 3.14+
- `uv` package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Run database migrations:
```bash
python manage.py migrate
```

3. Import existing CSV data:
```bash
python manage.py import_csv
```

4. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Open your browser and visit:
   - Dashboard: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Usage

### Importing Data

To import or update job market data from the CSV file:

```bash
python manage.py import_csv
```

To clear existing data and import fresh:

```bash
python manage.py import_csv --clear
```

To import from a custom CSV file:

```bash
python manage.py import_csv --file path/to/your/data.csv
```

### Automated Scraping

The project includes GitHub Actions workflows that automatically scrape job data daily and update the CSV file.

## Project Structure

- `jobmarket_watch/` - Django project settings
- `dashboard/` - Main Django app with models, views, and templates
- `data/` - CSV data files and scraping notebooks
- `.github/workflows/` - GitHub Actions for automated scraping

## To Dos

- [x] scrapper
- [x] plotly viz
- [x] github action
- [x] simple django setup
- [x] data into sqlite
- [x] frontend