from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from braces.views import LoginRequiredMixin, FormValidMessageMixin

from headcount.forms import HeadcountUserCreationForm
from . import forms
from . import models


class Dashboard(LoginRequiredMixin, generic.ListView):
    model = models.Event
    template_name = 'events/dashboard.html'

    def get_queryset(self):
        return self.model.objects.by_host(host=self.request.user).upcoming()


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
    slug_field = 'shortid'
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
    slug_field = 'shortid'
    success_url = reverse_lazy('events:dashboard')

    def get_queryset(self):
        return self.model.objects.by_host(host=self.request.user).upcoming()

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('OK, we deleted the event and notified any'
                                    '"yes" or "maybe" RSVPs'))
        return super(DeleteEvent, self).delete(request, *args, **kwargs)


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


class EventDetailRSVP(LoginRequiredMixin, FormValidMessageMixin,
                      generic.CreateView):
    form_class = forms.RSVPForm
    form_valid_message = u'Thanks for RSVPing!'
    model = models.RSVP

    def dispatch(self, request, *args, **kwargs):
        """
        If a user who has already rsvp gets here, redirect them to the
        update view.
        """
        try:
            rsvp = self.model.objects.select_related('event').get(
                event__shortid=kwargs.get('slug'), user=request.user)
        except self.model.DoesNotExist:
            return super(EventDetailRSVP, self).dispatch(
                request, *args, **kwargs)

        return HttpResponseRedirect(
            reverse_lazy('events:update_rsvp',
                         kwargs={'slug': rsvp.event.shortid}))

    def get_context_data(self, **kwargs):
        """
        Add event to context.
        If requesting user is the host, don't display an rsvp form.
        """
        context = super(EventDetailRSVP, self).get_context_data(**kwargs)
        context.update({'event': self.get_event()})

        if self.request.user == context['event'].host:
            del context['form']

        return context

    def get_form_kwargs(self):
        """ Add event and user to the form """
        kwargs = super(EventDetailRSVP, self).get_form_kwargs()
        kwargs.update({'event': self.get_event(), 'user': self.request.user})
        return kwargs

    def get_event(self):
        return get_object_or_404(models.Event, shortid=self.kwargs.get('slug'))

    def get_success_url(self):
        return self.get_event().get_absolute_url()


class RSVPUpdate(LoginRequiredMixin, FormValidMessageMixin,
                 generic.UpdateView):
    form_class = forms.RSVPForm
    form_valid_message = u'Your RSVP has been updated!'
    model = models.RSVP

    def get_success_url(self):
        return reverse_lazy(
            'events:update_rsvp',
            kwargs={'slug': self.get_object().event.shortid})

    def get_context_data(self, **kwargs):
        context = super(RSVPUpdate, self).get_context_data(**kwargs)
        context.update({'event': self.get_object().event})
        return context

    def get_object(self, queryset=None):
        try:
            return self.model.objects.select_related('event').get(
                event__shortid=self.kwargs.get('slug'),
                user=self.request.user)
        except self.model.DoesNotExist:
            raise Http404
