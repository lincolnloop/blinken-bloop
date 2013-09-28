from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView

from authtools.forms import UserCreationForm
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


class EventWizard(SessionWizardView):
    template_name = 'home.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        kwargs.update({
            'form_list': [
                forms.EventForm,
                UserCreationForm
            ]
        })
        return super(EventWizard, cls).as_view(*args, **kwargs)

    def done(self, form_list, **kwargs):
        event_form = form_list[0]
        user_form = form_list[1]

        new_user = user_form.save()
        event = event_form.save(commit=False)
        event.host = new_user
        event.save()

        user = authenticate(username=new_user.email,
                            password=user_form.cleaned_data.get('password1'))
        if user is not None:
            login(self.request, user)

        messages.success(
            self.request, _('Your event and account have been created!'))

        return HttpResponseRedirect(reverse_lazy('events:dashboard'))
