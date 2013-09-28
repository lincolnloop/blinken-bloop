from django.core.exceptions import ValidationError
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
            venue_name=u'Test Venue',
            address=u'1 Infinite Loop',
            city=u'Cupertino',
            state=u'California',
            latitude=37.33174,
            longitude=-122.03033,
            max_attendees=20,
            max_guests=1,
            cost=u'Free',
            start=arrow.utcnow().datetime,
            end=arrow.utcnow().replace(days=+1).datetime
        )

        self.assertTrue(isinstance(event, models.Event))
        self.assertIn(u'<strong>', event.description_html)


class RSVPModelTests(TestCase):
    def create_event(self):
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
        return event

    def test_creation(self):
        event = self.create_event()

        rsvp = models.RSVP.objects.create(
            event=event,
            num_guests=0,
            response=models.RSVP.RESPONSE_CHOICES.yes,
            name=u'Test Testerson',
            email=u'test@example.com'
        )

        self.assertTrue(isinstance(rsvp, models.RSVP))
        self.assertIn(rsvp, event.rsvps.all())

    def test_too_many_guests(self):
        event = self.create_event()
        rsvp = models.RSVP.objects.create(
            event=event,
            num_guests=100,
            response=models.RSVP.RESPONSE_CHOICES.yes,
            name=u'Too Many Guests',
            email=u'icantcount@example.com'
        )
        with self.assertRaises(ValidationError):
            rsvp.clean()
