from django.shortcuts import render
from django.db.models import Max, Min, Avg
from .models import JobData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def index(request):
    """Main dashboard view with overview and visualizations"""
    
    # Get summary statistics
    latest_date = JobData.objects.aggregate(Max('date'))['date__max']
    total_jobs = 0
    cities = []
    
    if latest_date:
        latest_data = JobData.objects.filter(date=latest_date).order_by('-job_count')
        cities = list(latest_data.values())
        total_jobs = sum(city['job_count'] for city in cities)
    
    # Get all data for plotting
    all_data = JobData.objects.all().order_by('date', 'location')
    df = pd.DataFrame(list(all_data.values()))
    
    # Create time series chart
    time_series_chart = None
    if not df.empty:
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
        time_series_chart = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # Create bar chart for latest data
    latest_bar_chart = None
    if cities:
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
        
        latest_bar_chart = fig_bar.to_html(full_html=False, include_plotlyjs='cdn')
    
    context = {
        'latest_date': latest_date,
        'total_jobs': total_jobs,
        'cities': cities,
        'time_series_chart': time_series_chart,
        'latest_bar_chart': latest_bar_chart,
    }
    
    return render(request, 'dashboard/index.html', context)


def city_detail(request, location):
    """Detailed view for a specific city"""
    
    city_data = JobData.objects.filter(location=location).order_by('date')
    df = pd.DataFrame(list(city_data.values()))
    
    chart_html = None
    stats = {}
    
    if not df.empty:
        # Calculate statistics
        stats = {
            'current': df.iloc[-1]['job_count'] if len(df) > 0 else 0,
            'average': df['job_count'].mean(),
            'max': df['job_count'].max(),
            'min': df['job_count'].min(),
            'latest_date': df.iloc[-1]['date'] if len(df) > 0 else None,
        }
        
        # Create line chart
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
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    context = {
        'location': location,
        'stats': stats,
        'chart': chart_html,
        'city_data': list(city_data.values()),
    }
    
    return render(request, 'dashboard/city_detail.html', context)
