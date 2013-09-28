from django.test import TestCase

import arrow
from authtools.models import User

from .. import models


class EventModelTests(TestCase):
    def setUp(self):
        self.user = User(email="test@example.com")
        self.user.set_unusable_password()
        self.user.save()

    def test_creation(self):
        event = models.Event.objects.create(
            host=self.user,
            title="Test Event",
            description="A test event with some **markdown**",
            max_attendees=20,
            max_guests=1,
            cost="Free",
            start=arrow.utcnow().datetime,
            end=arrow.utcnow().replace(days=+1).datetime
        )

        self.assertTrue(isinstance(event, models.Event))
