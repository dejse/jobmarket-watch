from django.contrib import admin
from .models import JobData


@admin.register(JobData)
class JobDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'location', 'job_count']
    list_filter = ['date', 'location']
    search_fields = ['location']
    date_hierarchy = 'date'
    ordering = ['-date', 'location']
