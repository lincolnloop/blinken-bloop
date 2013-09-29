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

    def test_home_page_anon(self):
        """ Anon user should see form wizard page. """
        url = reverse('events:home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_auth(self):
        """ Authenticated user should be forwarded to event creation page. """
        self._login_user()
        url = reverse('events:home')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_event_detail_edit_only_accessible_by_owner(self):
        """
        Test that event owner is the only person who can
        access the edit page.
        """
        evil_user = self._create_user(email=u'evil@example.com')
        self._login_user(email=evil_user.email)

        url = reverse('events:edit', kwargs={'slug': self.event.shortid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_event_detail_accesible_by_owner(self):
        self._login_user()
        url = reverse('events:edit', kwargs={'slug': self.event.shortid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
