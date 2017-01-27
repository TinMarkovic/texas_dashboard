"""
View endpoints for Survey
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from urllib import unquote

from texas_dashboard.models import DashboardNotification, LOModule
from texas_dashboard.utils import hide_notification_for_user, put_module_in_progress_for_user


@login_required
def manage_notifications(request, notification_name):
    """
    Notification management endpoint.

    Currently only removing notifications is allowed (and it only hides them from user)
    """
    notification_name = unquote(notification_name)

    try:
        notification = DashboardNotification.get(notification_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        hide_notification_for_user(notification, request.user)
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)


@login_required
def manage_modules(request, module_name):
    """
    LOModule management endpoint.

    Currently only removing notifications is allowed (and it only hides them from user)
    """
    module_name = unquote(module_name)

    try:
        module = LOModule.get(module_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "PUT":
        put_module_in_progress_for_user(module, request.user)
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)
