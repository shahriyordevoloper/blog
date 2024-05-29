# filters.py
from datetime import datetime, timedelta
from django.db.models import Count
from rest_framework import filters
from django.utils import timezone


class LastMonthFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Calculate the date range for the last month
        today = timezone.now()
        last_month_start = today - timedelta(days=today.day)
        last_month_end = today - timedelta(days=today.day, seconds=1)

        # Filter objects based on the date range
        queryset = queryset.filter(date__range=(last_month_start, last_month_end))
        
        return queryset

