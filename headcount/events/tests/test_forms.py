from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase

import arrow
from authtools.models import User

from .. import models
from .. import forms
from .test_models import create_user


class EventFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            'start_0': '10/05/2016',
            'start_1': '7:00 AM',
            'end_0': '10/05/2016',
            'end_1': '12:00 PM',
            'title': 'Test Event',
            'description': '## Test Event',
            'location': 'My House',
            'max_attendees': 20,
            'max_guests': 1
        }

    def test_valid(self):
        host = create_user()
        data = self.form_data.copy()
        data.update({'host': host.pk})
        form = forms.EventForm(data)
        self.assertTrue(form.is_valid())
