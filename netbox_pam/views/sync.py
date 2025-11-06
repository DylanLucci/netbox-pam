from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

from ..models import UserGroup
from ..utils import *


class JumpcloudSyncView(View):
    template_name = 'netbox_pam/sync.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        usergroups = fetch_jumpcloud_usergroups()
        created_count = 0
        updated_count = 0
        status_lines = []

        for ug in usergroups:
            name = ug.get('name')
            comments = ug.get('description')

            if not name:
                continue

            obj, created = UserGroup.objects.get_or_create(
                name=name,
                defaults={
                    'comments': comments,
                },
            )

            if not created and obj.comments != comments:
                obj.comments = comments
                obj.save()
                updated_count += 1
                status_lines.append(f"Updated existing group: {name}")
            elif created:
                created_count += 1
                status_lines.append(f"Created new group: {name}")
            else:
                status_lines.append(f"Skipping existing group: {name}")

        html = render_to_string("netbox_pam/inc/sync_status.html", {
            'status_lines': status_lines,
            'created_count': created_count,
            'updated_count': updated_count,
        })
        return HttpResponse(html)

    # TODO: Statistics e.g., last ran, number of synced objects, what went wrong, etc.
