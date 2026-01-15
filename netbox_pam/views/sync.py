import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views import View

from core.choices import JobStatusChoices
from core.models import Job

from ..jobs import SyncJob


class JumpcloudSyncView(View):
    template_name = 'netbox_pam/sync.html'

    def get_required_permission(self):
        return 'netbox_pam.sync_jumpcloud'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        job = Job.objects.create(
            name='Jumpcloud Sync Job',
            job_id=uuid.uuid4(),
            user=request.user,
            scheduled=now(),
            interval=5,
        )
        runner = SyncJob(job)
        result = runner.run()
        job.status = JobStatusChoices.STATUS_COMPLETED
        job.save()
        html = render_to_string("netbox_pam/inc/sync_status.html", result)
        return HttpResponse(html)

    # TODO: Statistics e.g., last ran, number of synced objects, what went wrong, etc.
