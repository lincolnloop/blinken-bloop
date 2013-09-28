from django.test import TestCase

import arrow
from authtools.models import User

from .. import models


def create_user(email=u'test@example.com'):
    user = User(email=email)
    user.set_unusable_password()
    user.save()
    return user


class EventModelTests(TestCase):
    def test_creation(self):
        user = create_user()
        event = models.Event.objects.create(
            host=user,
            title=u'Test Event',
            description=u'A test event with some **markdown**',
            max_attendees=20,
            max_guests=1,
            cost=u'Free',
            start=arrow.utcnow().datetime,
            end=arrow.utcnow().replace(days=+1).datetime
        )

        self.assertTrue(isinstance(event, models.Event))
        self.assertIn(u'<strong>', event.description_html)


class RSVPModelTests(TestCase):
    def test_creation(self):
        user = create_user()
        event = models.Event.objects.create(
            host=user,
            title=u'Test Event',
            description=u'A test event with some **markdown**',
            max_attendees=20,
            max_guests=1,
            cost=u'Free',
            start=arrow.utcnow().datetime,
            end=arrow.utcnow().replace(days=+1).datetime
        )

        rsvp = models.RSVP.objects.create(
            event=event,
            num_guests=0,
            response=models.RSVP.RESPONSE_CHOICES.yes,
            name=u'Test Testerson',
            email=u'test@example.com'
        )

        self.assertTrue(isinstance(rsvp, models.RSVP))
        self.assertIn(rsvp, event.rsvps.all())
