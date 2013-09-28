from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView, View

from braces.views import LoginRequiredMixin

from . import forms
from . import models


class Home(FormView):
    form_class = forms.EventForm
    success_url = reverse_lazy('events:dashboard')
    template_name = 'home.html'


class Dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('DASHBOARD!')
