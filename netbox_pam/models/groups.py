from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel

__all__ = (
    'DeviceGroup',
    'UserGroup',
)


class DeviceGroup(PrimaryModel):
    """
    An arbitrary collection of Devices.
    """
    name = models.CharField(
        max_length=64,
        verbose_name=_('Name')
    )
    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='device_groups',
        verbose_name=_('Devices')
    )
    vms = models.ManyToManyField(
        to='virtualization.VirtualMachine',
        related_name='device_groups',
        verbose_name=_('Virtual Machines')
    )

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_unique_name'
            ),
        )
        verbose_name = _('Device Group')
        verbose_name_plural = _('Device Groups')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_pam:devicegroup', args=[self.pk])


class UserGroup(PrimaryModel):
    """
    An arbitrary collection of Users (Contacts).
    """
    name = models.CharField(
        max_length=64,
        verbose_name=_('Name')
    )
    contacts = models.ManyToManyField(
        to='tenancy.Contact',
        related_name='user_groups',
        verbose_name=_('Contacts')
    )
    devicegroups = models.ManyToManyField(
        to='netbox_pam.DeviceGroup',
        related_name='user_groups',
        verbose_name=_('Device Groups')
    )

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_unique_name'
            ),
        )
        verbose_name = _('User Group')
        verbose_name_plural = _('User Groups')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_pam:usergroup', args=[self.pk])
