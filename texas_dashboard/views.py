"""
View endpoints for Survey
"""
import json
import base64

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseServerError, 
    HttpResponseNotFound, HttpResponseForbidden
)
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from texas_dashboard.models import DashboardNotification, LOModule
from texas_dashboard.utils import (
    hide_notification_for_user, put_module_in_progress_for_user, read_notification_for_user,
    delete_all_sessions_by_user, get_userid_by_email, emit_dashboard_event, acquire_extra_data,
    module_to_dict
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
        if put_module_in_progress_for_user(module, request.user):
            emit_dashboard_event("txoc.dashboard.module_put_in_progress", {
                "module": module_to_dict(module),
                "user_oidc_extra_data": acquire_extra_data(request.user)
            })
    else:
        return HttpResponseServerError("Not Implemented")

    return HttpResponse()  # 200 for OK :)


@csrf_exempt
def logout_user(request):
    """
    Logout user across all sessions.
    """
    whitelisted_providers = (
        "tex.extensionengine.com", 
        "oidc.tex.extensionengine.com",
    )
    provider = request.get_host()

    if provider not in whitelisted_providers:
        return HttpResponseForbidden()
    
    token = str(request.body).split("=")[1]
    base64_content = token.split(".")[1]

    # Python's decode base64 is somewhat too sensitive
    missing_padding = len(base64_content) % 4
    if missing_padding != 0:
        base64_content += b'='* (4 - missing_padding)
    content = base64.b64decode(base64_content)

    json_data = json.loads(content)

    try:
        user_email = str(json_data["email"])
    except KeyError:
        return HttpResponseServerError("Malformed data!")

    try:    
        delete_all_sessions_by_user( get_userid_by_email(user_email))
    except Exception as ex:
        return HttpResponseServerError(ex)

    return HttpResponse()  # 200 for OK :)


@login_required
def record_event(request):
    """
    Event emitter for the dashboard.
    """
    event_dict = dict()

    event_dict["user_oidc_extra_data"] = acquire_extra_data(request.user)

    if request.method == 'GET':
        return HttpResponseNotFound()

    json_data = json.loads(request.body)
    try:
        event_data = json_data["event_data"]
        event_name = json_data["event_name"]
    except KeyError:
        return HttpResponseServerError("Malformed data!")

    if "module_id" in event_data:
        event_dict["module"] = module_to_dict(LOModule.get(event_data["module_id"]))

    emit_dashboard_event(event_name, event_dict)

    return HttpResponse()  # 200 for OK :)
