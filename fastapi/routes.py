"""Route handlers for dashboard views"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from typing import Optional

from database import get_latest_date, get_latest_data, get_all_data, get_city_data
from charts import create_time_series_chart, create_bar_chart, create_city_trend_chart

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard view with overview and visualizations"""
    
    # Get summary statistics
    latest_date = get_latest_date()
    total_jobs = 0
    cities = []
    
    if latest_date:
        cities = get_latest_data()
        total_jobs = sum(city['job_count'] for city in cities)
    
    # Get all data for plotting
    all_data = get_all_data()
    
    # Create time series chart
    time_series_chart = None
    if all_data:
        time_series_chart = create_time_series_chart(all_data)
    
    # Create bar chart for latest data
    latest_bar_chart = None
    if cities:
        latest_bar_chart = create_bar_chart(cities, latest_date)
    
    context = {
        'request': request,
        'latest_date': latest_date,
        'total_jobs': total_jobs,
        'cities': cities,
        'time_series_chart': time_series_chart,
        'latest_bar_chart': latest_bar_chart,
    }
    
    return templates.TemplateResponse('index.html', context)


@router.get("/city/{location}", response_class=HTMLResponse)
async def city_detail(request: Request, location: str):
    """Detailed view for a specific city"""
    
    city_data = get_city_data(location)
    
    chart_html = None
    stats = {}
    
    if city_data:
        # Convert to pandas for statistics calculation
        df = pd.DataFrame(city_data)
        
        # Calculate statistics
        stats = {
            'current': int(df.iloc[-1]['job_count']) if len(df) > 0 else 0,
            'average': float(df['job_count'].mean()),
            'max': int(df['job_count'].max()),
            'min': int(df['job_count'].min()),
            'latest_date': df.iloc[-1]['date'] if len(df) > 0 else None,
        }
        
        # Create line chart
        chart_html = create_city_trend_chart(city_data, location)
    
    context = {
        'request': request,
        'location': location,
        'stats': stats,
        'chart': chart_html,
        'city_data': city_data,
    }
    
    return templates.TemplateResponse('city_detail.html', context)
