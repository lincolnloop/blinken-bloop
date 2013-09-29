from django.test import TestCase

from authtools.models import User

from .test_forms import create_event


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = self._create_user()
        self.event = create_event()

    def _create_user(self, username=u'test@example.com'):
        return User.objects.create(
            username=username,
            password='test123'
        )

    def _login_user(self, username='test@example.com', password='test123'):
        self.assertTrue(
            self.client.login(username=username, password=password))
