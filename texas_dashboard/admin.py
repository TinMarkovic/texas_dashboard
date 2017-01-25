"""
Provide accessors to these models via the Django Admin pages
"""

from django.contrib import admin
from texas_dashboard.models import DashboardNotification

admin.site.register(DashboardNotification)
