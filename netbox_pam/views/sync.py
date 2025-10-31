from django.shortcuts import redirect, render
from django.views import View

from ..utils import *


class JumpcloudSyncView(View):
    template_name = 'netbox_pam/sync.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        users = fetch_jumpcloud_users()

        for user in users:
            name = user.get('firstname') + ' ' + user.get('lastname')
            email = user.get('email')
            print(f"Fetching user {name} with email {email}")

        return redirect('tenancy:contact_list')
