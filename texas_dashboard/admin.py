"""
Provide accessors to these models via the Django Admin pages
"""

from django.contrib import admin
from texas_dashboard.models import DashboardNotification, LOModule

admin.site.register(DashboardNotification)
admin.site.register(LOModule)
