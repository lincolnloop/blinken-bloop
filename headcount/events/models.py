from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

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

    def __unicode__(self):
        return self.title
