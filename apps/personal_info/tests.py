# -*- coding: utf-8 -*-
"""
    Functional tests for my application
"""
import os

from PIL import Image
from StringIO import StringIO

from django.test import TestCase
from django.test import RequestFactory
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.http import HttpRequest

from apps.personal_info.models import Person
from apps.personal_info.middleware import RequestLogMiddleware
from apps.personal_info.models import WebRequest
from fortytwo_test_task.settings import BASE_DIR

Image.init()


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


class EditPageTest(TestCase):
    """ The edit page test case """

    def setUp(self):
        """ Initialize some test data"""
        image = Image.open(
            StringIO(open(
                os.path.join(
                    BASE_DIR,
                    'assets',
                    'img',
                    'test_large.jpg'
                )
            ).read()
            ),
        )
        image_file = StringIO()
        image.save(image_file, format='JPEG', quality=90)
        self.uploaded_file = InMemoryUploadedFile(
            image_file,
            None,
            'test.jpg',
            'image/jpeg',
            image_file.len,
            None
        )
        self.client.login(
            username='admin',
            password='admin'
        )

    def test_image(self):
        """
        Test whether images are scaled to proper size and
        deleted from /uploads/ upon removal
        """
        person = Person.objects.first()
        person.picture = self.uploaded_file
        person.save()
        self.assertEqual(Person.objects.first().picture.width, 200)
        self.assertEqual(Person.objects.first().picture.height, 200)
        path = person.picture.path
        person.picture.delete()
        person.save()
        self.assertFalse(os.path.exists(path))

    def test_user_login(self):
        """ Test whether the anonymous user is redirected to login page """
        response = self.client.get(reverse('update'))
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.client.logout()
        response = self.client.get(reverse('update'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('personal_info/login.html')

    def test_page_correct_person(self):
        """ Ensure that the edit page displays correct person """
        response = self.client.get(reverse('update'))
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.assertIn('Paul', response.content)
        self.assertIn('Pukach', response.content)
        self.assertIn('1996-06-25', response.content)
        self.assertIn(
            'Student of AM faculty in Lviv Polytechnic National University',
            response.content
        )
        self.assertIn('pavlopukach@gmail.com', response.content)
        self.assertIn('icebreaker454@jabber.me', response.content)
        self.assertIn('shoker2506', response.content)
        self.assertIn('Phone: +380963699598', response.content)

    def test_form_valid(self):
        """ Test the form with posting valid data """
        response = self.client.post(
            reverse('update'),
            {
                # All required fields are posted
                'first_name': 'Alan',
                'last_name': 'Walker',
                'birth_date': '1990-07-12',
                'contacts_email': 'awalker@gmail.com',
            }
        )
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alan', response.content)
        self.assertIn('Walker', response.content)
        self.assertIn('1990-07-12', response.content)
        self.assertIn("awalker@gmail.com", response.content)

    def test_form_invalid(self):
        """ Test the form with posting invalid data """
        response = self.client.post(
            reverse('update'),
            {
                # Not all required fields are posted
                "first_name": "Alan",
                "last_name": "Walker"
            }
        )
        # After form error we must see the same page with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            'birth_date',
            'This field is required.'
        )
        self.assertFormError(
            response,
            'form',
            'contacts_email',
            'This field is required.'
        )

        response = self.client.post(
            reverse('update'),
            {
                # All required fields are posted
                "first_name": "Alan",
                "last_name": "Walker",
                "birth_date": "some invalid date",
                "contacts_email": "some invalid email"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            'birth_date',
            'Enter a valid date.'
        )
        self.assertFormError(
            response,
            'form',
            'contacts_email',
            'Enter a valid email address.'
        )
