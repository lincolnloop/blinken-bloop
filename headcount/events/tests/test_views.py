from django.core.urlresolvers import reverse
from django.test import TestCase

from authtools.models import User

from .test_forms import create_event


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = self._create_user()
        self.event = create_event(self.user)

    def _create_user(self, email=u'test@example.com'):
        return User.objects.create_user(
            name='Tester McTesterson',
            email=email,
            password='test123',
            is_active=True
        )

    def _login_user(self, email=u'test@example.com', password=u'test123'):
        self.assertTrue(
            self.client.login(email=email, password=password))

    def test_home_page(self):
        url = reverse('events:home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
