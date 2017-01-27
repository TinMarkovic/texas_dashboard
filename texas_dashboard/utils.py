from texas_dashboard.models import DashboardNotification, DashboardUserNotificationStatus, LOModuleUserStatus, LOModule


def get_notifications_list_for_user(user):
    active_notifications = DashboardNotification.objects.filter(active=True)
    hidden_user_notifications = DashboardUserNotificationStatus.objects.filter(user=user, show=False)

    hidden_notifications = [o.notification for o in hidden_user_notifications]
    notifications_to_display = [notification for notification in active_notifications
                                if notification not in hidden_notifications]

    return notifications_to_display


def get_grouped_modules_for_user(user):
    modules = LOModule.objects.filter(active=True)
    in_progress_user_modules = LOModuleUserStatus.objects.filter(user=user, in_progress=True)

    in_progress_modules = [o.module for o in in_progress_user_modules]
    fresh_modules = [module for module in modules if module not in in_progress_modules]

    return fresh_modules, in_progress_modules


def hide_notification_for_user(notification, user):
    status = DashboardUserNotificationStatus.objects.get_or_create(notification=notification, user=user)
    status.show = False
    status.save(update_fields=['show'])


def put_module_in_progress_for_user(module, user):
    module = LOModuleUserStatus.objects.get_or_create(notification=module, user=user)
    module.in_progress = True
    module.save(update_fields=['in_progress'])
