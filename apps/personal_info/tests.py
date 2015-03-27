# -*- coding: utf-8 -*-
"""
    Functional tests for my application
"""

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest

from apps.personal_info.models import Person
from apps.personal_info.middleware import RequestLogMiddleware
from apps.personal_info.models import WebRequest


class MainPageTest(TestCase):
    """ The personal_info index page test case """
    fixtures = ['test.json']

    def test_person_model_unicode(self):
        """ Test the Person model unicode """
        person = Person.objects.first()
        self.assertEqual(
            person.__unicode__(),
            "%s %s" % (
                person.first_name,
                person.last_name
            )
        )

    def test_person_model_names(self):
        """ Test Person model verbose names """
        self.assertEqual(Person._meta.verbose_name, u'Person')
        self.assertEqual(Person._meta.verbose_name_plural, u'Persons')

    def test_database(self):
        """ Test whether there is only one object in the database """
        queryset = Person.objects.all()
        if len(queryset) > 1:
            self.fail("There shouldn't be another database entry")

    def test_multiple_db_records(self):
        """ Test the page if there are additional Person objects """
        other_obj = Person.objects.create(
            first_name=u'Alan',
            last_name=u'Walker',
            birth_date='1990-10-10',
            contacts_email='alanwalker@gmail.com'
        )
        other_obj.save()
        response = self.client.get(reverse_lazy('home'))
        self.assertNotIn('Alan', response.content)

    def test_auth(self):
        """ Test the authentication system"""
        user = User.objects.first()
        self.client.login(username=user.username, password=user.password)

    def test_page_info(self):
        """ Test whether the page displays data """
        response = self.client.get(reverse_lazy('home'))

        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.assertIn('John', response.content)
        self.assertIn('Smith', response.content)
        self.assertIn('July 12, 1990', response.content)
        self.assertIn('FBI agent', response.content)
        self.assertIn('jsmith@gmail.com', response.content)
        self.assertIn('jsmith@jabber.me', response.content)
        self.assertIn('jsmith_007', response.content)
        self.assertIn('Phone: +39912034', response.content)


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

    def test_time_ordering(self):
        """ Test the requests ordering by time """
        requests = WebRequest.objects.order_by('-time')
        response = self.client.get(reverse('requests'))

        for i, request in enumerate(requests):
            self.assertEqual((response.context['requests'])[i].pk, request.pk)

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
        Test whether the /favicon.ico requests are being ignored
        """
        request = HttpRequest()
        request.path = '/favicon.ico'
        request.method = 'GET'
        self.middleware.process_request(request)
        response = self.client.get('/requests/')
        self.assertNotIn(request.path, response.content)

