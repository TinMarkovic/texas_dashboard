Texas OnCourse Dashboard Backend
================================

Installation
============

On the machine, as the `edxapp` user, run:

`pip install git+https://github.com/TinMarkovic/texas_dashboard.git`

After that, you have to configure two files from the edx-platform repo: 

- lms/envs/common.py (adding to installed_apps)
- lms/urls.py (adding a valid path to the app)

```
# Edit in common.py

INSTALLED_APPS = (
	...

    # Custom Texas OnCourse dashboard backend
    'texas_dashboard',
    )

MIDDLEWARE_CLASSES = (
    ...

    # Custom Texas OnCourse middleware
    'texas_dashboard.middleware.SessionLinkingMiddleware',
    )

# Edit in urls.py

urlpatterns = (
	...

    # URLs for custom Texas OnCourse dashboard
    url(r'^txoc/', include('texas_dashboard.urls', namespace='txoc')),
    )
```

Then, run Django migrations.


API endpoints
=============

``` 
	POST /txoc/logout #  Takes JSON with "user_id" field and logs out user
    PUT /txoc/notifications/list/  # Takes list of notifications and marks as read
    PUT /txoc/notifications/(?P<notification_id>[0-9]+)/  # Marks as read
    DELETE /txoc/notifications/(?P<notification_id>[0-9]+)/  # Deletes for user
    PUT /txoc/lomodules/(?P<module_id>[0-9]+)/  # Marks as read
```

Util methods
============

```
    get_grouped_modules_for_user(user)
        return new_notifications, read_notifications
    get_notifications_list_for_user(user)
        return fresh_modules, in_progress_modules
```