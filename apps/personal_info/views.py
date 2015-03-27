# -*- coding: utf-8 -*-
"""
    This is the views module for the personal_info project
"""

import logging
import simplejson

from django.views.generic import TemplateView
from django.views.generic import ListView

from apps.personal_info.models import Person
from apps.personal_info.models import WebRequest

LOGGER = logging.getLogger('personal_info')


class IndexView(TemplateView):
    """ The index view for personal_info """
    template_name = 'personal_info/index.html'

    def dispatch(self, request, *args, **kwargs):
        """
        The method that catches the request to log it
        :param request: the request
        :param args: arguments
        :param kwargs: keyword arguments
        :return: returns the base class dispatch()
        """
        LOGGER.info(request.path)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        The method that adds template context
        :param kwargs: keyword arguments
        :return: context for the given template
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        # Selecting the first object, for the data is only for myself
        person = Person.objects.first()
        if person:
            LOGGER.debug(person.__unicode__())
        context['person'] = person
        return context


class RequestsView(ListView):
    """
        The requests page view for my application
    """
    template_name = 'personal_info/requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        queryset = WebRequest.objects.order_by('-time')[:10]
        for obj in queryset:
            LOGGER.debug(obj.__unicode__())
        return queryset