# -*- coding: utf-8 -*-
"""
    This is the views module for the personal_info project
"""

import logging

from django.views.generic import TemplateView
from django.views.generic import ListView

from apps.personal_info.models import Person
from apps.personal_info.models import WebRequest

LOGGER_INFO = logging.getLogger('personal_info.info')
LOGGER_DEBUG = logging.getLogger('personal_info.debug')


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
        LOGGER_INFO.info(request.path)
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
            LOGGER_DEBUG.debug(person.__unicode__())
        context['person'] = person
        return context


class RequestsView(ListView):
    """
        The requests page view for my application
    """
    template_name = 'personal_info/requests.html'
    context_object_name = 'requests'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden method that logs the request
        :param request: the request that comes in
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """
        LOGGER_INFO.info(request.path)
        return super(RequestsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        The method that gets the QuerySet for the ListView
        :return: QuerySet for the view
        """
        queryset = WebRequest.objects.order_by('time')[:10]
        for obj in queryset:
            LOGGER_DEBUG.debug(obj.__unicode__())
        return queryset

    def get_context_data(self, **kwargs):
        """
        The method to add context data
        :param kwargs: keyword arguments
        :return: page context
        """
        context = super(RequestsView, self).get_context_data(**kwargs)
        context['requests_count'] = WebRequest.objects.count()
        return context
