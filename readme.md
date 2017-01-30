Texas OnCourse Dashboard Backend
================================

API endpoints
=============

"""
    DELETE /txoc/notifications/(?P<notification_id>[0-9]+)/
    PUT /txoc/lomodules/(?P<module_id>[0-9]+)/
"""

Util methods
============

"""
    get_grouped_modules_for_user(user)
        return notifications_to_display
    get_notifications_list_for_user(user)
        return fresh_modules, in_progress_modules
"""