# -*- coding: utf-8 -*-
"""
This module contains functional tests for the
personal_info application's user edit page
"""

import os

from PIL import Image
from StringIO import StringIO

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.personal_info.models import Person
from fortytwo_test_task.settings import BASE_DIR

Image.init()


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
