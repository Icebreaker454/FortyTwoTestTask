"""
This module contains functional tests for the requests
priority edit page
"""
from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.personal_info.models import WebRequest


class RequestsPriorityPageTest(TestCase):
    """
    This class is the requests priority edit page
    test case
    """
    def setUp(self):
        """
        Initializing test data
        :return:
        """
        self.client.login(username='admin', password='admin')
        for _ in range(2):
            WebRequest.objects.create(remote_address='test')

    def test_auth(self):
        """
        Test whether the page has the authentication system
        :return:
        """
        response = self.client.get(reverse('requests_edit'))
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.client.logout()
        response = self.client.get(reverse('requests_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('personal_info/login.html')

    def test_changing_priority(self):
        """
        Test the AJAX priority editing
        :return:
        """
        response = self.client.get(reverse('requests_edit'))
        old_priority = response.context['requests'][0].priority
        request_id = response.context['requests'][0].id
        self.client.post(
            reverse('requests_edit'),
            {
                'pk': request_id,
                'priority': old_priority + 1
            },
            **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'
            }
        )
        self.assertEqual(
            WebRequest.objects.get(pk=request_id).priority,
            old_priority + 1
        )
