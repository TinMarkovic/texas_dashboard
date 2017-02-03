"""
URL mappings for the Texas OnCourse features
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'texas_dashboard.views',

    url(r'^notifications/list$', 'manage_multiple_notifications', name='manage_multiple_notifications'),
    url(r'^notifications/(?P<notification_id>[0-9]+)/$', 'manage_notifications', name='manage_notifications'),
    url(r'^lomodules/(?P<module_id>[0-9]+)/$', 'manage_modules', name='manage_modules'),
    url(r'^logout$', 'logout_user', name='logout_user'),
)
