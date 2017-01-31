Texas OnCourse Dashboard Backend
================================

Installation
============

On the machine, as the `edxapp` user, run:

`pip install *git+url*`

After that, you have to configure two files from the edx-platform repo: 

- common.py (adding to installed_apps)
- urls.py (adding a valid path to the app)

Then, run migrations.

TODO: Improve readme :)



API endpoints
=============

``` 
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