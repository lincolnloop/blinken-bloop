from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from authtools.views import LogoutView
from braces.views import LoginRequiredMixin, FormValidMessageMixin

from headcount.forms import HeadcountUserCreationForm
from . import forms
from . import models


class Dashboard(LoginRequiredMixin, generic.ListView):
    model = models.Event
    template_name = 'events/dashboard.html'

    def get_queryset(self):
        return self.model.objects.filter(host=self.request.user)


class CreateEvent(LoginRequiredMixin, FormValidMessageMixin,
                  generic.CreateView):
    form_class = forms.EventForm
    form_valid_message = u'Your event was created!'
    model = models.Event
    success_url = reverse_lazy('events:dashboard')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CreateEvent, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'show_actions': True,
        })
        return kwargs

    def get_initial(self):
        initial = super(CreateEvent, self).get_initial()
        initial.update({'host': self.request.user.pk})
        return initial


class UpdateEvent(LoginRequiredMixin, FormValidMessageMixin,
                  generic.UpdateView):
    form_class = forms.EventForm
    form_valid_message = u'Your event was updated!'
    model = models.Event
    success_url = reverse_lazy('events:dashboard')

    def get_queryset(self):
        return self.model.objects.by_host(host=self.request.user).upcoming()

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UpdateEvent, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'show_actions': True,
        })
        return kwargs


class DeleteEvent(LoginRequiredMixin, generic.DeleteView):
    model = models.Event
    success_url = reverse_lazy('events:dashboard')

    def get_queryset(self):
        return self.model.objects.by_host(host=self.request.user).upcoming()


class EventWizard(SessionWizardView):
    template_name = 'home.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        kwargs.update({
            'form_list': [
                forms.EventForm,
                HeadcountUserCreationForm
            ]
        })
        return super(EventWizard, cls).as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('events:create'))
        return super(EventWizard, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, step):
        return {
            'render_form_tag': False,
            'show_actions': False
        }

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


class EventDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Event
