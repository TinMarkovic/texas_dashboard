"""
Models to support Texas OnCourse dashboard features
"""

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from student.models import User
from model_utils.models import TimeStampedModel


class DashboardNotification(TimeStampedModel):
    """
    Model for the answers that a user gives for a particular form in a course
    """
    name = models.CharField(max_length=255)
    content = models.TextField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get(cls, id_number):
        """
        Helper class method to look up a Dashboard Notification,
        raises ObjectDoesNotExist if the id is invalid.
        """

        exists = DashboardNotification.objects.filter(id=id_number).exists()
        if exists:
            notification = DashboardNotification.objects.get(id=id_number)
        else:
            raise ObjectDoesNotExist()
        return notification


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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_title = models.CharField(max_length=255, null=True, blank=True)
    module_image_small = models.ImageField(null=True, blank=True)
    module_image_large = models.ImageField(null=True, blank=True)
    url = models.TextField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get(cls, id_number):
        """
        Helper class method to look up a Dashboard Notification,
        raises ObjectDoesNotExist if the id is invalid.
        """

        exists = LOModule.objects.filter(id=id_number).exists()
        if exists:
            module = LOModule.objects.get(id=id_number)
        else:
            raise ObjectDoesNotExist()
        return module


class LOModuleUserStatus(models.Model):
    """
    LO Modules' status for a user on the dashboard.
    """
    user = models.ForeignKey(User, db_index=True)
    module = models.ForeignKey(LOModule, db_index=True)
    in_progress = models.BooleanField(default=False)
