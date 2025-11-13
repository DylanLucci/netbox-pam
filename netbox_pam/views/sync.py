import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from dcim.models import Device
from tenancy.models import Contact

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
        status_lines = []
        created_count, updated_count = 0, 0

        # Sync Contacts
        for user in fetch_jumpcloud_users(limit=10):
            result = self._sync_contact(user)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync User Groups
        for group in fetch_jumpcloud_usergroups(limit=0):
            result = self._sync_usergroup(group)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync Devices
        for device in fetch_jumpcloud_devices(limit=10):
            # result = self._sync_device(device)
            # status_lines.append(result['message'])
            # created_count += result['created']
            # updated_count += result['updated']
            # result = self._sync_device(device)
            # print(fetch_jumpcloud_device_memberships(device, limit=10))
            pass

        # Sync Device Groups
        for group in fetch_jumpcloud_devicegroups(limit=0):
            result = self._sync_devicegroup(group)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']
            # print(json.dumps(group, indent=4))

        # Sync Device Groups bound to User Groups
        for usergroup in UserGroup.objects.all():
            result = self._sync_usergroup_devicegroups(usergroup)
            status_lines.append(result['message'])

        html = render_to_string("netbox_pam/inc/sync_status.html", {
            'status_lines': status_lines,
            'created_count': created_count,
            'updated_count': updated_count,
        })
        return HttpResponse(html)

    def _sync_contact(self, user):
        name = f"{user.get('firstname')} {user.get('lastname')}".strip()
        email = user.get('email')
        if not name and not email:
            return {'message': 'Skipped user with no name or email', 'created': 0, 'updated': 0}

        lookup = {'email__iexact': email} if email else {'name': name}
        field_map = {
            'name': name,
            'title': user.get('jobTitle'),
            'phone': _fetch_phone_numbers(user.get('phoneNumbers')),
            'email': email,
            'address': _fetch_addresses(user.get('addresses')),
            'description': user.get('description'),
        }
        custom_fields = {
            'pam_jc_id': user.get('id'),
            'pam_ssh_keys': user.get('ssh_keys'),
        }

        return sync_object(Contact, lookup, field_map, custom_fields)

    def _sync_usergroup(self, group):
        name = group.get('name')
        if not name:
            return {'message': 'Skipped unnamed user group', 'created': 0, 'updated': 0}

        lookup = {'name': name}
        field_map = {
            'name': name,
            'comments': group.get('description'),
        }
        custom_fields = {
            'pam_jc_id': group.get('id'),
        }

        return sync_object(UserGroup, lookup, field_map, custom_fields)

    def _sync_device(self, device):
        pass

    def _sync_devicegroup(self, group):
        name = group.get('name')
        if not name:
            return {'message': 'Skipped unnamed device group', 'created': 0, 'updated': 0}
        group_id = group.get('id')
        memberships = fetch_jumpcloud_devicegroup_memberships(group_id)
        matched_devices = []
        missing_devices = []

        for membership in memberships:
            jc_device_id = membership.get('to', {}).get('id')
            if not jc_device_id:
                continue

            device = Device.objects.filter(custom_field_data__pam_jc_id=jc_device_id).first()
            if device:
                matched_devices.append(device)
            else:
                missing_devices.append(jc_device_id)

            print(matched_devices)

        return sync_object(
            DeviceGroup,
            {'name': name},
            {'comments': group.get('description')},
            {'pam_jc_id': group_id},
        )

    def _sync_usergroup_devicegroups(self, usergroup):
        jc_usergroup_id = usergroup.custom_field_data.get('pam_jc_id')
        if not jc_usergroup_id:
            return {
                'message': f"Skipped UserGroup '{usergroup}' (no Jumpcloud ID)",
                'created': 0,
                'updated': 0,
            }

        memberships = fetch_jumpcloud_usergroup_devicegroups(jc_usergroup_id)
        matched_groups = []
        missing_groups = []

        for membership in memberships:
            jc_devicegroup_id = membership.get('to', {}).get('id')
            if not jc_devicegroup_id:
                continue

            devicegroup = DeviceGroup.objects.filter(custom_field_data__pam_jc_id=jc_devicegroup_id).first()
            if devicegroup:
                matched_groups.append(devicegroup)
            else:
                missing_groups.append(jc_devicegroup_id)

        if matched_groups:
            usergroup.devicegroups.add(*matched_groups)

        return {
            'message': f"Linked {len(matched_groups)} device groups to UserGroup '{usergroup.name}'",
            'linked_count': len(matched_groups),
            'missing_count': len(missing_groups),
            'missing_ids': missing_groups,
        }

    # TODO: Statistics e.g., last ran, number of synced objects, what went wrong, etc.
