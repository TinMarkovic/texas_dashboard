from texas_dashboard.models import (
    DashboardNotification, DashboardUserNotificationStatus, LOModuleUserStatus, LOModule, UserSession
)
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import connection

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def get_notifications_list_for_user(user):
    active_notifications = DashboardNotification.objects.filter(active=True)
    user_notifications = DashboardUserNotificationStatus.objects.filter(user=user)
    hidden_user_notifications = user_notifications.filter(show=False).order_by('-notification_id')
    read_user_notifications = user_notifications.filter(seen=True).order_by('-notification_id')

    hidden_notifications = [o.notification for o in hidden_user_notifications]
    read_notifications = [o.notification for o in read_user_notifications]

    displayed_notifications = []
    new_notifications = []
    for notification in active_notifications:
        if notification in hidden_notifications:
            pass
        elif notification in read_notifications:
            displayed_notifications.append(notification)
        else:
            new_notifications.append(notification)

    return new_notifications, displayed_notifications


def get_grouped_modules_for_user(user):
    modules = LOModule.objects.filter(active=True)
    in_progress_user_modules = LOModuleUserStatus.objects.filter(user=user, in_progress=True)

    in_progress_modules = [o.module for o in in_progress_user_modules]
    fresh_modules = [module for module in modules if module not in in_progress_modules]

    return fresh_modules, in_progress_modules


def hide_notification_for_user(notification, user):
    status, created = DashboardUserNotificationStatus.objects.get_or_create(notification=notification, user=user)
    status.seen = True
    status.show = False
    status.save(update_fields=['show'])


def read_notification_for_user(notification, user):
    status, created = DashboardUserNotificationStatus.objects.get_or_create(notification=notification, user=user)
    status.seen = True
    status.save(update_fields=['seen'])


def put_module_in_progress_for_user(module, user):
    module, created = LOModuleUserStatus.objects.get_or_create(module=module, user=user)
    module.in_progress = True
    module.save(update_fields=['in_progress'])


def delete_all_sessions_by_user(user):
    user_session_links = UserSession.objects.filter(user_id=user)
    #user_sessions = [SessionStore(o.session) for o in user_session_links]
    #user_sessions = [Session.objects.get(session_key=o.session) for o in user_session_links]
    user_sessions = [o.session for o in user_session_links]
    print "Inside function..."
    print user_sessions
    for session in user_sessions:
        print "Deleting:"
        print session
        try:
            # session.delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM edxapp.django_session WHERE session_key=%s;", [session])
        except Exception as ex:
            print ex


def create_session_user_link(session_key, user_id):
    UserSession.objects.get_or_create(session=session_key, user_id=user_id)
