from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

import misaka

from model_utils import Choices
from model_utils.models import TimeStampedModel, TimeFramedModel


class Event(TimeStampedModel, TimeFramedModel):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="events")
    title = models.CharField(_("Event name"), max_length=500)
    description = models.TextField(
        _("Event description"),
        help_text=_("You should include contact details in the description. "
                    "Markdown is supported."))
    description_html = models.TextField(blank=True, editable=False)
    max_attendees = models.PositiveIntegerField(
        _("Max # of attendees"), blank=True,
        help_text=_("Leave blank for no limit"), null=True)
    max_guests = models.PositiveIntegerField(
        _("Max # of guests per attendee"), blank=True,
        help_text=_("Leave blank for no limit"), null=True)
    cost = models.CharField(_("Event cost"), blank=True, default='',
                            max_length=150)

    class Meta:
        ordering = ['start', 'end', 'title']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Event, self).save(*args, **kwargs)


class RSVP(TimeStampedModel):
    RESPONSE_CHOICES = Choices(
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe')
    )
    event = models.ForeignKey(Event, related_name="rsvps")
    num_guests = models.PositiveIntegerField(
        _("How many guests are you bringing?"), default=0)
    response = models.CharField(
        _("Are you coming?"), choices=RESPONSE_CHOICES, max_length=10)
    name = models.CharField(_("Your name"), max_length=255)
    email = models.EmailField(_("Your email"))
    notes = models.TextField(_("Any notes for the organizer"), blank=True)

    class Meta:
        verbose_name = _("RSVP")
        verbose_name_plural = _("RSVPs")

    def clean(self):
        if self.num_guests > self.event.max_guests:
            raise ValidationError(
                _("The event only allows {0.event.max_guests} "
                  "guest(s).".format(self)))
