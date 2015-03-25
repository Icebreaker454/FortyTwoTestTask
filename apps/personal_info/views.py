# -*- coding: utf-8 -*-
"""
    This is the views module for the personal_info project
"""

from django.views.generic import TemplateView

from apps.personal_info.models import Person


class IndexView(TemplateView):
    """ The index view for personal_info """
    template_name = 'personal_info/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # Selecting the first object, for the data is only for myself
        person = Person.objects.first()
        context['person'] = person
        return context
