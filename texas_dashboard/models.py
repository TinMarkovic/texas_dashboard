"""
Models to support Texas OnCourse dashboard features
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from student.models import User
from model_utils.models import TimeStampedModel


class DashboardNotification(TimeStampedModel):
    """
    Model for the answers that a user gives for a particular form in a course
    """
    name = models.CharField(max_length=255, db_index=True)
    content = models.TextField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class DashboardUserNotificationStatus(TimeStampedModel):
    """
    Certain Users Notifications status.
    """
    user = models.ForeignKey(User, db_index=True)
    notification = models.ForeignKey(DashboardNotification, db_index=True)
    show = models.BooleanField(default=True)


class LOModule(models.Model):
    """
    LO Modules to display on the dashboard.
    """
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    description_title = models.CharField(max_length=255, null=True, blank=True)
    module_image_small = models.ImageField(null=True, blank=True)
    module_image_large = models.ImageField(null=True, blank=True)
    url = models.TextField()

    def __unicode__(self):
        return self.name


class LOModuleUserStatus(models.Model):
    """
    LO Modules' status for a user on the dashboard.
    """
    user = models.ForeignKey(User, db_index=True)
    module = models.ForeignKey(LOModule, db_index=True)
    in_progress = models.BooleanField(default=False)
