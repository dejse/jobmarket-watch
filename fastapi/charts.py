"""Plotly chart generation for job market data"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any, Optional


def create_time_series_chart(data: List[Dict[str, Any]]) -> Optional[str]:
    """
    Create a time series line chart showing job counts over time by location
    
    Args:
        data: List of dictionaries with keys: date, location, job_count
    
    Returns:
        HTML string of the chart, or None if no data
    """
    if not data:
        return None
    
    df = pd.DataFrame(data)
    
    if df.empty:
        return None
    
    fig = px.line(
        df,
        x='date',
        y='job_count',
        color='location',
        title='Job Count Over Time by Location',
        labels={'date': 'Date', 'job_count': 'Job Count', 'location': 'Location'},
        markers=True,
        template='plotly_white',
    )
    
    fig.update_layout(
        hovermode='x unified',
        font=dict(family='Arial, sans-serif', size=12),
        title_font=dict(size=18, color='#2C3E50'),
        xaxis_title_font=dict(size=14, color='#34495E'),
        yaxis_title_font=dict(size=14, color='#34495E'),
        height=500,
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='white',
    )
    
    fig.update_traces(line=dict(width=2.5))
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def create_bar_chart(cities: List[Dict[str, Any]], latest_date: str) -> Optional[str]:
    """
    Create a bar chart showing current job counts by city
    
    Args:
        cities: List of dictionaries with keys: location, job_count
        latest_date: The date for the title
    
    Returns:
        HTML string of the chart, or None if no data
    """
    if not cities:
        return None
    
    fig_bar = px.bar(
        cities,
        x='location',
        y='job_count',
        title=f'Current Job Count by City ({latest_date})',
        labels={'location': 'City', 'job_count': 'Job Count'},
        template='plotly_white',
        color='job_count',
        color_continuous_scale='Blues',
    )
    
    fig_bar.update_layout(
        showlegend=False,
        height=400,
        font=dict(family='Arial, sans-serif', size=12),
        title_font=dict(size=18, color='#2C3E50'),
    )
    
    return fig_bar.to_html(full_html=False, include_plotlyjs='cdn')


def create_city_trend_chart(city_data: List[Dict[str, Any]], location: str) -> Optional[str]:
    """
    Create a line chart showing job count trend for a specific city
    
    Args:
        city_data: List of dictionaries with keys: date, job_count
        location: City name for the title
    
    Returns:
        HTML string of the chart, or None if no data
    """
    if not city_data:
        return None
    
    df = pd.DataFrame(city_data)
    
    if df.empty:
        return None
    
    fig = px.line(
        df,
        x='date',
        y='job_count',
        title=f'Job Count Trend for {location}',
        labels={'date': 'Date', 'job_count': 'Job Count'},
        markers=True,
        template='plotly_white',
    )
    
    fig.update_layout(
        height=500,
        font=dict(family='Arial, sans-serif', size=12),
        title_font=dict(size=18, color='#2C3E50'),
        showlegend=False,
    )
    
    fig.update_traces(line=dict(width=3, color='#3498db'))
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
