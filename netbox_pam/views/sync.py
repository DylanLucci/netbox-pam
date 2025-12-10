import json
import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views import View
from virtualization.models import VirtualMachine

from core.models import Job
from dcim.models import Device
from tenancy.models import Contact

from ..jobs import *
from ..models import DeviceGroup, UserGroup
from ..utils import *


def _fetch_addresses(addresses):
    address_lines = []
    for addr in addresses:
        if not any(addr.values()):
            continue

        parts = [
            addr.get('type').capitalize(),
            addr.get('streetAddress'),
            addr.get('locality'),
            addr.get('region'),
            addr.get('postalCode'),
            addr.get('country')
        ]

        line = ", ".join(filter(None, parts))
        address_lines.append(line)

    address = "\n".join(address_lines) if address_lines else ""
    return address

def _fetch_phone_numbers(phone_numbers):
    phone = next((pn.get('number') for pn in phone_numbers if pn.get('number')), "")
    return phone

class JumpcloudSyncView(View):
    template_name = 'netbox_pam/sync.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        job = Job.objects.create(
            name='Jumpcloud Sync Job',
            job_id=uuid.uuid4(),
            user=request.user,
            scheduled=now(),
            interval=1440,
        )
        sync_job(job=job)
        status_lines = []
        created_count, updated_count = 0, 0

        # TODO: Sync Devices
        for device in fetch_jumpcloud_devices(limit=50):
            result = self._sync_device(device)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync Contacts
        for user in fetch_jumpcloud_users(limit=50):
            result = self._sync_contact(user)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync Device Groups
        for devicegroup in fetch_jumpcloud_devicegroups(limit=50):
            result = self._sync_devicegroup(devicegroup)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync User Groups
        for usergroup in fetch_jumpcloud_usergroups(limit=50):
            result = self._sync_usergroup(usergroup)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        html = render_to_string("netbox_pam/inc/sync_status.html", {
            'status_lines': status_lines,
            'created_count': created_count,
            'updated_count': updated_count,
        })
        return HttpResponse(html)

    def _sync_device(self, device):
        name = device.get('displayName')
        if not name:
            return {'message': 'Skipped unnamed virtual machine', 'created': 0, 'updated': 0}
        jc_id = device.get('id')

        lookup = {'custom_field_data__pam_jc_id': jc_id} if jc_id else {'name': name}
        # device_field_map = {
        #     'name': name,
        # }
        vm_field_map = {
            'name': name,
        }
        custom_fields = {
            'pam_jc_id': jc_id,
        }
        return sync_object(VirtualMachine, lookup, vm_field_map, custom_fields)
        # return sync_object(Device, lookup, device_field_map, custom_fields)

    def _sync_devicegroup(self, group):
        name = group.get('name')
        if not name:
            return {'message': 'Skipped unnamed device group', 'created': 0, 'updated': 0}
        jc_id = group.get('id')

        lookup = {'custom_field_data__pam_jc_id': jc_id} if jc_id else {'name': name}
        field_map = {
            'name': name,
            'comments': group.get('description'),
        }
        custom_fields = {
            'pam_jc_id': jc_id,
        }

        # TODO: Sync member devices

        result = sync_object(DeviceGroup, lookup, field_map, custom_fields)
        devicegroup = result['instance']

        old_vm_ids = set(devicegroup.vms.values_list('id', flat=True))

        jc_vms = fetch_jumpcloud_devicegroup_memberships(jc_id)
        remote_ids = [
            m.get("to", {}).get("id")
            for m in jc_vms
            if m.get("to", {}).get("id")
        ]

        local_vms = VirtualMachine.objects.filter(
            custom_field_data__pam_jc_id__in=remote_ids
        )
        devicegroup.vms.set(local_vms)

        new_vm_ids = set(local_vms.values_list("id", flat=True))
        if old_vm_ids != new_vm_ids:
            result['updated'] = 1
            result['message'] = (
                f'Updated device group members: '
                f'<a href="{devicegroup.get_absolute_url()}">{devicegroup.name}</a>'
            )

        return result

    def _sync_contact(self, user):
        name = f"{user.get('firstname')} {user.get('lastname')}".strip()
        email = user.get('email')
        if not name and not email:
            return {'message': 'Skipped user with no name or email', 'created': 0, 'updated': 0}
        jc_id = user.get('id')

        lookup = {'custom_field_data__pam_jc_id': jc_id} or {'email__iexact': email} if email else {'name': name}
        field_map = {
            'name': name,
            'title': user.get('jobTitle'),
            'phone': _fetch_phone_numbers(user.get('phoneNumbers')),
            'email': email,
            'address': _fetch_addresses(user.get('addresses')),
            'description': user.get('description'),
        }
        custom_fields = {
            'pam_jc_id': jc_id,
            'pam_ssh_keys': user.get('ssh_keys'),
        }

        return sync_object(Contact, lookup, field_map, custom_fields)

    def _sync_usergroup(self, group):
        name = group.get('name')
        if not name:
            return {'message': 'Skipped unnamed user group', 'created': 0, 'updated': 0}
        jc_id = group.get('id')

        lookup = {'custom_field_data__pam_jc_id': jc_id} if jc_id else {'name': name}
        field_map = {
            'name': name,
            'comments': group.get('description'),
        }
        custom_fields = {
            'pam_jc_id': jc_id,
        }

        result = sync_object(UserGroup, lookup, field_map, custom_fields)
        usergroup = result['instance']

        jc_devicegroups = fetch_jumpcloud_usergroup_devicegroups(jc_id)
        local_dgs = DeviceGroup.objects.filter(
            custom_field_data__pam_jc_id__in=[dg['id'] for dg in jc_devicegroups]
        )
        usergroup.devicegroups.set(local_dgs)

        old_contact_ids = set(usergroup.contacts.values_list('id', flat=True))

        jc_contacts = fetch_jumpcloud_usergroup_memberships(jc_id)
        remote_ids = [
            c.get('to', {}).get('id')
            for c in jc_contacts
            if c.get('to', {}).get('id')
        ]

        local_contacts = Contact.objects.filter(
            custom_field_data__pam_jc_id__in=remote_ids
        )
        usergroup.contacts.set(local_contacts)

        new_contact_ids = set(local_contacts.values_list('id', flat=True))
        if old_contact_ids != new_contact_ids:
            result['updated'] = 1
            result['message'] = (
                f'Updated device group members: '
                f'<a href="{usergroup.get_absolute_url()}">{usergroup.name}</a>'
            )

        return result

    # TODO: Statistics e.g., last ran, number of synced objects, what went wrong, etc.
