"""
URL mappings for the Texas OnCourse features
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'texas_dashboard.views',

    url(r'^notifications/(?P<notification_name>[^/]+)/$', 'manage_notifications', name='remove_notification'),
    url(r'^lomodules/(?P<module_name>[^/]+)/$', 'manage_modules', name='manage_modules'),
)
