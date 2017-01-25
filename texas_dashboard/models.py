"""
Models to support Texas OnCourse dashboard features
"""

from django.db import models
from student.models import User
from model_utils.models import TimeStampedModel


class DashboardNotification(TimeStampedModel):
    """
    Model for the answers that a user gives for a particular form in a course
    """
    name = models.CharField(max_length=255, db_index=True)
    content = models.TextField()
    active = models.BooleanField()


class DashboardUserNotificationStatus(TimeStampedModel):
    """
    Certain Users Notifications status.
    """
    user = models.ForeignKey(User, db_index=True)
    notification = models.ForeignKey(DashboardNotification, db_index=True)
    show = models.BooleanField()

