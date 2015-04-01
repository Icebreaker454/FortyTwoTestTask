"""
This module contains functional tests for the
personal_info application management commands
"""
from StringIO import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.db import models


class CommandsTest(TestCase):
    """
    This class is the personal_info management commands
    test case
    """
    def setUp(self):
        """
        Initialize testing data
        """
        self.out_file = StringIO()
        self.err_file = StringIO()

        models_list = models.get_models()

        self.model_data = [
            '%s %s' % (
                model.__name__,
                model.objects.count()
            ) for model in models_list
        ]

    def test_call_command(self):
        """
        Test the whole command functionality
        """
        call_command(
            'modeloutput',
            stdout=self.out_file,
            stderr=self.err_file
        )

        self.out_file.seek(0)
        self.err_file.seek(0)

        self.assertEqual(
            len(self.out_file.readlines()),
            len(self.err_file.readlines())
        )

        self.out_file.seek(0)
        self.err_file.seek(0)

        for model_data_entry in self.model_data:
            line = self.out_file.readline()
            error_line = self.err_file.readline()
            self.assertEqual('error: %s' % line, error_line)
            data = line.strip().split('-')
            self.assertIn(data[0], model_data_entry)
            self.assertIn(data[1], model_data_entry)

        self.out_file.seek(0)
        self.err_file.seek(0)

        self.assertEqual(
            len(self.out_file.readlines()),
            len(self.model_data)
        )
