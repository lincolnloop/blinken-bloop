from django.test import TestCase

import arrow
from authtools.models import User

from .. import forms
from .. import models
from .test_models import create_user


def create_event(host):
    return models.Event.objects.create(
        host=host,
        title=u'Test Event',
        description=u'A test event with some **markdown**',
        location=u'1 Infinite Loop, Cupertino, CA',
        max_attendees=20,
        max_guests=1,
        cost=u'Free',
        start=arrow.utcnow().replace(days=+1).datetime,
        end=arrow.utcnow().replace(days=+2).datetime
    )


class EventFormTests(TestCase):
    def setUp(self):
        self.host = create_user()
        self.form_data = {
            'start_0': '10/05/2016',
            'start_1': '7:00 AM',
            'end_0': '10/05/2016',
            'end_1': '12:00 PM',
            'title': 'Test Event',
            'description': '## Test Event',
            'location': 'My House',
            'max_attendees': 20,
        }

    def test_valid(self):
        form = forms.EventForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_dates(self):
        data = self.form_data.copy()
        data.update({'end_0': '10/04/2016'})
        form = forms.EventForm(data)
        self.assertFalse(form.is_valid())


class RSVPFormTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.event = create_event(self.user)
        self.form_data = {
            'event': self.event.pk,
            'user': self.user.pk,
            'response': u'yes',
            'num_guests': 1
        }

    def test_valid(self):
        form = forms.RSVPForm(data=self.form_data, event=self.event,
                              user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.party_size, 2)
        form.save()
        self.assertEqual(form.instance.event.total_coming, 2)

    def test_event_full(self):
        self.event.max_attendees = 3
        self.event.save()
        self.mean_user = create_user(email=u'mean@example.com')
        rsvp = models.RSVP.objects.create(
            event=self.event,
            user=self.mean_user,
            response=u'yes',
            num_guests=1
        )
        self.assertIsInstance(rsvp, models.RSVP)

        form = forms.RSVPForm(data=self.form_data, event=self.event,
                              user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0],
                         "We're sorry, there are only 1 space(s) left.")
