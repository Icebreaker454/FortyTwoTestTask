"""
This module contains functional tests for the
personal_info application requests page
"""


from django.test import TestCase
from django.test import RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import reverse

from apps.personal_info.middleware import RequestLogMiddleware
from apps.personal_info.models import WebRequest


class RequestsPageTest(TestCase):
    """ The requests page test case """
    def setUp(self):
        self.middleware = RequestLogMiddleware

    def test_middleware_saves_requests(self):
        """
        Test whether the middleware stores requests in db
        """
        request = HttpRequest()

        request.path = '/some_path'
        request.method = 'GET'
        request.META['REMOTE_ADDR'] = 'localhost'

        self.middleware.process_request(request)
        self.assertEqual(WebRequest.objects.count(), 1)

    def test_request_ordering(self):
        """ Test the requests ordering by priority and time """
        requests = WebRequest.objects.order_by('priority', 'time')[:10]
        response = self.client.get(reverse('requests'))

        for i, request in enumerate(requests):
            self.assertEqual((response.context['requests'])[i].pk, request.pk)

    def test_request_adding_priority(self):
        """
        Test whether adding priority to the field makes
        effect on the database
        """
        first = WebRequest.objects.create(remote_address='test1')
        second = WebRequest.objects.create(remote_address='test2')
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.context['requests'][0].pk, first.pk)
        second.priority = 1
        second.save()
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.context['requests'][0].pk, second.pk)

    def test_request_model_unicode(self):
        """ Test the request model string representation"""
        request = WebRequest.objects.create(
            remote_address='http://localhost',
            path='/testpath'
        )
        self.assertEqual(
            request.__unicode__(),
            "%s%s" % (request.remote_address, request.path)
        )

    def test_page_requests_count(self):
        """" Test whether the page has only 10 requests shown on it """
        for _ in range(10):
            self.client.get(reverse('requests'))

        response = self.client.get(reverse('requests'))
        self.assertTrue(len(response.context['requests']) <= 10)
        self.assertIn(reverse('requests'), response.content, 10)

    def test_filter_requests(self):
        """
        Test whether the /favicon.ico requests and ajax requests to
        the requests page are being ignored
        """
        request = HttpRequest()
        request.path = '/favicon.ico'
        request.method = 'GET'
        self.middleware.process_request(request)
        response = self.client.get(reverse('requests'))
        self.assertNotIn(request.path, response.content)

    def test_filter_self_ajax(self):
        """
        Test whether the ajax requests from the requests page are being
        ignored
        """
        factory = RequestFactory()
        request_count = WebRequest.objects.count()
        request = factory.get(
            '/requests/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.middleware.process_request(request)
        self.assertEqual(request_count, WebRequest.objects.count())
