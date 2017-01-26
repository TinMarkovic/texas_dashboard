from texas_dashboard.models import DashboardNotification, DashboardUserNotificationStatus


def get_notifications_list_for_user(user):
    active_notifications = DashboardNotification.objects.filter(active=True)
    hidden_user_notifications = DashboardUserNotificationStatus.objects.filter(user=user, show=False)
    notifications_to_display = [notification for notification in active_notifications
                                if notification not in hidden_user_notifications]
    return notifications_to_display


def hide_notification_for_user(notification, user):
    status = DashboardUserNotificationStatus.objects.get_or_create(notification=notification, user=user)
    status.show = False
    status.save()
