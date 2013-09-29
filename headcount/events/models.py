import random as _random
import string

try:
    random = _random.SystemRandom()
except NotImplementedError:
    random = _random.Random()

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _

import arrow
import misaka

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel, TimeFramedModel

from . import signals


def get_shortid(length=6, alphabet=string.letters + string.digits):
    return u''.join([random.choice(alphabet) for i in xrange(length)])


class EventQuerySet(models.query.QuerySet):
    def by_host(self, host):
        return self.filter(host=host)

    def upcoming(self):
        return self.filter(start__gt=arrow.utcnow().datetime)

    def past(self):
        return self.filter(end__lt=arrow.utcnow().datetime)

    def current(self):
        now = arrow.utcnow().datetime
        return self.filter(start__lte=now, end__gte=now)


class RSVPQuerySet(models.query.QuerySet):
    def yes(self):
        return self.filter(response=RSVP.RESPONSE_CHOICES.yes)

    def no(self):
        return self.filter(response=RSVP.RESPONSE_CHOICES.no)

    def maybe(self):
        return self.filter(response=RSVP.RESPONSE_CHOICES.maybe)

    def possible(self):
        return self.exclude(response=RSVP.RESPONSE_CHOICES.no)


class Event(TimeStampedModel, TimeFramedModel):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             related_name='events')
    title = models.CharField(_('Event title:'),
                             max_length=500)
    description = models.TextField(
        _("What's the event about?"),
        help_text=_('You should include contact details in the description. '
                    'Markdown is supported.'))
    description_html = models.TextField(blank=True, editable=False)
    location = models.CharField(
        _("Where's the event?"),
        help_text=_("Address, IRC channel, or just 'My house'"),
        max_length=750)
    latitude = models.FloatField(blank=True, editable=False, null=True)
    longitude = models.FloatField(blank=True, editable=False, null=True)
    max_attendees = models.PositiveIntegerField(
        _('How many people total?'), blank=True,
        help_text=_('Leave blank for no limit'), null=True)
    max_guests = models.PositiveIntegerField(
        _('How many guests can people bring?'), blank=True,
        help_text=_('Leave blank for no limit'), null=True)
    cost = models.CharField(_('Do people need to bring anything, or pay?'),
                            blank=True, default='', max_length=150)
    shortid = models.CharField(blank=True, default='', max_length=10)
    objects = PassThroughManager.for_queryset_class(EventQuerySet)()

    class Meta:
        ordering = ['start', 'end', 'title']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        self.shortid = get_shortid()

        try:
            while Event.objects.get(shortid=self.shortid):
                self.shortid = get_shortid()
        except Event.DoesNotExist:
            pass

        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('events:detail', kwargs={'slug': self.shortid})

    @property
    def total_coming(self):
        """ Return total number of poeple coming """
        return sum(
            [peep.num_guests + 1 for peep in self.rsvps.possible()])


class RSVP(TimeStampedModel):
    RESPONSE_CHOICES = Choices(
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe')
    )
    event = models.ForeignKey(Event, related_name='rsvps')
    num_guests = models.PositiveIntegerField(
        _('How many guests are you bringing?'), default=0)
    response = models.CharField(
        _('Are you coming?'), choices=RESPONSE_CHOICES, max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rsvps')
    notes = models.TextField(_('Any notes for the organizer'), blank=True)
    objects = PassThroughManager.for_queryset_class(RSVPQuerySet)()

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = _('RSVP')
        verbose_name_plural = _('RSVPs')

    def clean(self):
        if self.event.max_guests and self.num_guests > self.event.max_guests:
            raise ValidationError(
                _('The event only allows {0.event.max_guests} '
                  'guest(s).'.format(self)))

models.signals.post_save.connect(signals.event_creation, sender=Event)
models.signals.post_save.connect(signals.event_change, sender=Event)
models.signals.pre_delete.connect(signals.event_delete, sender=Event)
models.signals.post_save.connect(signals.rsvp_creation, sender=RSVP)
