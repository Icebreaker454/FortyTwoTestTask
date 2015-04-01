"""
This module contains tests for the
personal_info application template tags
"""
from django.test import TestCase
from django.template import Template
from django.template import Context
from django.template import TemplateSyntaxError
from django.core.urlresolvers import reverse

from apps.personal_info.models import Person


class TemplateTagsTest(TestCase):
    """
    This class is the test case for the
    personal_info application template tags
    """
    def test_model_get_admin_url(self):
        """
        Tests the implementation of models get_admin_url()
        method
        """
        person = Person.objects.first()
        info = (person._meta.app_label, person._meta.module_name)
        url = reverse('admin:%s_%s_change' % info, args=(person.pk,))
        self.assertEqual(url, person.get_admin_url())

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

    def test_tags_invalid_params(self):
        """
        Test the behaviour of out template tag when we parse
        something different of Model objects
        """
        not_a_model = 'Hello! I am NOT a model instance'
        template = Template(
            '{% load custom_tags %}{% edit_link object %}'
        )
        rendered = template.render(
            Context({'object': not_a_model})
        )

        self.assertEqual(rendered, '')

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
            '{% load custom_tags %}{% edit_link "quoted"object %}'
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
