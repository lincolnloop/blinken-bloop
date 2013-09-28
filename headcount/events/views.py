from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView

from braces.views import LoginRequiredMixin

from . import forms
from . import models


class Home(FormView):
    form_class = forms.EventForm
    success_url = reverse_lazy('events:dashboard')
    template_name = 'home.html'


class Dashboard(LoginRequiredMixin, ListView):
    model = models.Event
    template_name = 'events/dashboard.html'

    def get_queryset(self):
        return self.model.objects.filter(host=self.request.user)
