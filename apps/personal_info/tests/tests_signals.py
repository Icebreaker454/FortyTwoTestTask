"""
This module contains functional tests for the
personal_info application signal processors
"""
from django.test import TestCase

from apps.personal_info.models import ModelLog
from apps.personal_info.models import WebRequest
from apps.personal_info.models import Person


class SignalsTestCase(TestCase):
    """
    This class is the test case for testing the personal_info
    application signal_processors.
    """
    def setUp(self):
        """ Initialize test data """
        self.person = Person(
            'Paul',
            'Pukach',
            '25-06-1996',
            'pavlopukach@gmail.com'
        )

    def test_model_creation(self):
        """ Test whether the model creating log is stored """
        record_count = ModelLog.objects.count()
        WebRequest.objects.create()
        self.assertEqual(record_count + 1, ModelLog.objects.count())
        last_record = ModelLog.objects.last()
        self.assertEqual(last_record.action, 'CREATE')
        self.assertEqual(last_record.model, 'WebRequest')
        self.assertEqual(last_record.model_id, WebRequest.objects.last().id)

        Person.objects.create()
        self.assertEqual(record_count + 2, ModelLog.objects.count())
        last_record = ModelLog.objects.last()
        self.assertEqual(last_record.action, 'CREATE')
        self.assertEqual(last_record.model, 'Person')
        self.assertEqual(last_record.model_id, Person.objects.last().id)

    def test_model_deletion(self):
        """ Test whether the model deleting is stored """
        self.person.save()
        record_count = ModelLog.objects.count()
        Person.objects.last().delete()
        self.assertEqual(record_count + 1, ModelLog.objects.count())
        last_record = ModelLog.objects.last()
        self.assertEqual(last_record.action, 'DELETE')
        self.assertEqual(last_record.model, 'Person')
        self.assertEqual(last_record.model_id, self.person.id)

    def test_model_editing(self):
        """ Test whether the model editing log is stored """
        self.person.save()
        self.person.bio = "Yahoo"
        self.person.save()
        last_record = ModelLog.objects.last()
        self.assertEqual(last_record.action, 'UPDATE')
        self.assertEqual(last_record.model, 'Person')
        self.assertEqual(last_record.model_id, self.person.id)
