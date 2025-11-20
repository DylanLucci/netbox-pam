import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

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

        # TODO: Sync Devices
        # for device in fetch_jumpcloud_devices(limit=10):
        #     # result = self._sync_device(device)
        #     # status_lines.append(result['message'])
        #     # created_count += result['created']
        #     # updated_count += result['updated']
        #     # result = self._sync_device(device)
        #     # print(fetch_jumpcloud_device_memberships(device, limit=10))
        #     pass

        # Sync Contacts
        for user in fetch_jumpcloud_users(limit=10):
            result = self._sync_contact(user)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync Device Groups
        for devicegroup in fetch_jumpcloud_devicegroups(limit=10):
            result = self._sync_devicegroup(devicegroup)
            status_lines.append(result['message'])
            created_count += result['created']
            updated_count += result['updated']

        # Sync User Groups
        for usergroup in fetch_jumpcloud_usergroups(limit=10):
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
        pass

    def _sync_devicegroup(self, group):
        name = group.get('name')
        if not name:
            return {'message': 'Skipped unnamed device group', 'created': 0, 'updated': 0}
        jc_id = group.get('id')

        lookup = {'custom_field_data__pam_jc_id': jc_id} or {'name': name}
        field_map = {
            'name': name,
            'comments': group.get('description'),
        }
        custom_fields = {
            'pam_jc_id': jc_id,
        }

        return sync_object(DeviceGroup, lookup, field_map, custom_fields)

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

        lookup = {'custom_field_data__pam_jc_id': jc_id} or {'name': name}
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

        jc_members = fetch_jumpcloud_usergroup_memberships(jc_id)
        member_ids = set()
        for m in jc_members:
            for key in ('member_id', 'id', 'user_id', 'systemuser_id'):
                val = m.get(key)
                if val:
                    member_ids.add(val)
                    break

        if member_ids:
            parsed_ids = []
            for mid in member_ids:
                try:
                    parsed_ids.append(int(mid))
                except Exception:
                    parsed_ids.append(mid)

            local_contacts = list(Contact.objects.filter(custom_field_data__pam_jc_id__in=parsed_ids))

            present_ids = set()
            for c in local_contacts:
                cf = c.custom_field_data or {}
                val = cf.get('pam_jc_id')
                if val is not None:
                    try:
                        present_ids.add(int(val))
                    except Exception:
                        present_ids.add(val)

            missing_ids = [mid for mid in parsed_ids if mid not in present_ids]
            for mid in missing_ids:
                try:
                    jc_user = fetch_jumpcloud_user(mid)
                except Exception:
                    continue
                if not jc_user:
                    continue
                r = self._sync_contact(jc_user)
                local_contacts.append(r['instance'])

            usergroup.contacts.set(local_contacts)

        return result

    # TODO: Statistics e.g., last ran, number of synced objects, what went wrong, etc.
