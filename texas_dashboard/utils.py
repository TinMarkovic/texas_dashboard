from texas_dashboard.models import (
    DashboardNotification, DashboardUserNotificationStatus, LOModuleUserStatus, LOModule, UserSession
)
import logging
from importlib import import_module
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from social.apps.django_app.default.models import UserSocialAuth

from eventtracking import tracker

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
User = get_user_model()


def emit_dashboard_event(event_name, event_data):
    """
    Emit team events with the correct course id context.
    """
    tracker.get_tracker()
    tracker.emit(event_name, event_data)


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
    module_status, created = LOModuleUserStatus.objects.get_or_create(module=module, user=user)
    module_status.in_progress = True
    module_status.save(update_fields=['in_progress'])
    return created


def delete_all_sessions_by_user(user):
    user_session_links = UserSession.objects.filter(user_id=user)
    user_sessions = [SessionStore(o.session) for o in user_session_links]
    for session in user_sessions:
        session.delete()


def create_session_user_link(session_key, user_id):
    UserSession.objects.get_or_create(session=session_key, user_id=user_id)


def get_userid_by_email(user_email):
    return User.objects.get(email=user_email).id


def get_logout_location(user):
    id_token = acquire_id_token(user)
    return ("https://oidc.tex.extensionengine.com/op/session/end?id_token_hint=" +
            id_token +
            "&post_logout_redirect_uri=https%3A%2F%2Fwww.texasoncourse.org&state=logout")


def acquire_id_token(user):
    extra_data = acquire_extra_data(user)
    try:
        return extra_data["id_token"]
    except KeyError:
        logging.warning("User without extra_data['id_token'] field: " + str(user.id))
        return ""


def acquire_extra_data(user):
    try:
        user_social_auth = UserSocialAuth.objects.get(user_id=user.id)
        extra_data = user_social_auth.extra_data
    except AttributeError:
        logging.warning("User without extra_data field: " + str(user.id))
        return ""
    except ObjectDoesNotExist:
        logging.warning("User without UserSocialAuth object: " + str(user.id))
        return ""
    return extra_data


def module_to_dict(module):
    module_dict = model_to_dict(module)
    module_dict["module_image_small"] = module_dict["module_image_small"].url
    module_dict["module_image_large"] = module_dict["module_image_large"].url
    return module_dict
