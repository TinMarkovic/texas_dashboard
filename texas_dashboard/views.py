"""
View endpoints for Survey
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from texas_dashboard.models import DashboardNotification, LOModule
from texas_dashboard.utils import (
    hide_notification_for_user, put_module_in_progress_for_user, read_notification_for_user
)


@login_required
def manage_multiple_notifications(request):
    """
    Notification management endpoint for multiple notifications.
    """

    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            read_notification_ids = json_data["read_notifications"]
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        for notification_id in read_notification_ids:
            try:
                notification = DashboardNotification.get(notification_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Could not find notification by id: " + str(notification_id))
            read_notification_for_user(notification, request.user)
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)


@login_required
def manage_notifications(request, notification_id):
    """
    Notification management endpoint.

    Currently removing and reading notifications is allowed.
    """

    try:
        notification = DashboardNotification.get(notification_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        hide_notification_for_user(notification, request.user)
    elif request.method == "PUT":
        read_notification_for_user(notification, request.user)
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)


@login_required
def manage_modules(request, module_id):
    """
    LOModule management endpoint.

    Currently only removing notifications is allowed (and it only hides them from user)
    """

    try:
        module = LOModule.get(module_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "PUT":
        put_module_in_progress_for_user(module, request.user)
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)
