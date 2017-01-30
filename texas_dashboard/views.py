"""
View endpoints for Survey
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from texas_dashboard.models import DashboardNotification, LOModule
from texas_dashboard.utils import hide_notification_for_user, put_module_in_progress_for_user


@login_required
def manage_notifications(request, notification_id):
    """
    Notification management endpoint.

    Currently only removing notifications is allowed (and it only hides them from user)
    """

    try:
        notification = DashboardNotification.get(notification_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == "DELETE":
        hide_notification_for_user(notification, request.user)
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
