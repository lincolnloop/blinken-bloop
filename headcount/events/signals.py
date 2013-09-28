from django.contrib.sites.models import Site
from django.http import HttpRequest

from headcount.utils import generate_email


def event_creation(sender, instance, created, raw, **kwargs):
    if created:
        to_email = '{0.name} <{0.email}>'.format(instance.host)
        email = generate_email(
            'events/email/new_event',
            HttpRequest(),
            {
                'instance': instance,
                'domain': Site.objects.get_current().domain
            },
            to=(to_email,)
        )
        email.send(fail_silently=False)


def event_change(sender, instance, created, raw, **kwargs):
    if not created:
        to_emails = ['{0.name} <{0.email}>'.format(rsvp.user) for rsvp in
                     instance.rsvps.possible()]
        email = generate_email(
            'events/email/new_event',
            HttpRequest(),
            {
                'instance': instance,
                'domain': Site.objects.get_current().domain
            },
            to=to_emails
        )
        email.send(fail_silently=False)
