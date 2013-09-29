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

    def _login_user(self, username='', password=''):
        self.assertTrue(
            self.client.login(username=username, password=password))

    def _set_site_session_data(self, session, site):
        session['current_site'] = {
            'pk': site.pk,
            'name': site.name,
            'domain': site.domain
        }
        session.save()
