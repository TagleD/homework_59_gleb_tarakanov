from django.urls import reverse
from django.views.generic import CreateView

from webapp.forms import StatusForm
from webapp.models import Status


class StatusAddView(CreateView):
    template_name = 'status/status_create.html'
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('index')