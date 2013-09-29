from django.test import TestCase

from .test_forms import create_event
from .test_models import create_user


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.event = create_event()

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
