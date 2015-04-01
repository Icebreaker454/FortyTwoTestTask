"""
This module contains tests for the
personal_info application template tags
"""
from django.test import TestCase
from django.template import Template
from django.template import Context
from django.template import TemplateSyntaxError

from apps.personal_info.models import Person


class TemplateTagsTest(TestCase):
    """
    This class is the test case for the
    personal_info application template tags
    """
    def test_tag_valid_params(self):
        """
        Test the behaviour of the template tag with valid data
        """
        person = Person.objects.first()
        template = Template(
            '{% load custom_tags %}{% edit_link object %}'
        )
        rendered = template.render(
            Context({'object': person})
        )
        self.assertIn(person.get_admin_url(), rendered)

    def test_tags_syntax_errors(self):
        """
        Test whether the syntax errors are dispatched
        """
        render = lambda t: Template(t).render(Context())
        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load custom_tags %}{% edit_link object as for %}'
        )
        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load custom_tags %}{% edit_link if not %}'
        )
        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load custom_tags %}{% edit_link object asd qwd %}'
        )


