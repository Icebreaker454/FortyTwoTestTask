# -*- coding: utf-8 -*-
"""
This is the views module for the personal_info project
"""

import logging
import simplejson as json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import FormView
from django.views.generic import RedirectView

from apps.personal_info.forms import PersonUpdateForm
from apps.personal_info.forms import LogInForm
from apps.personal_info.models import Person
from apps.personal_info.models import WebRequest

LOGGER_INFO = logging.getLogger('personal_info.info')
LOGGER_DEBUG = logging.getLogger('personal_info.debug')


class LoginRequiredMixin(object):
    """
    Class that implements @login_required functionality
    into a class-based view
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class LogOutView(RedirectView):
    """ View that handles user logout """
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
            LOGGER_DEBUG.debug(
                'User {} logged out'.format(
                    self.request.user
                )
            )
        return reverse('home')


class LogInView(FormView):
    """ The login page view for personal_info """
    template_name = 'personal_info/login.html'
    form_class = LogInForm

    def form_valid(self, form):
        """
        Check username and password
        :param form: the form that is posted
        :return:
        """
        login(self.request, form.get_user())
        LOGGER_DEBUG.debug(
            'User {} authenticated'.format(
                self.request.user
            )
        )
        return super(LogInView, self).form_valid(form)

    def get_success_url(self):
        """
        This method gets the FormView success url
        :return: the FormView success url
        """
        return reverse('update')


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
        status = request.GET.get('status_message')
        if status:
            setattr(self, 'status_message', status)
            LOGGER_INFO.info("Found status message: %s" % status)
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
        if getattr(self, 'status_message', None):
            context['status_message'] = self.status_message
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
        queryset = WebRequest.objects.order_by('-priority', 'time')[:10]
        if self.request.GET.get('reverse'):
            queryset = queryset.reverse()
        LOGGER_DEBUG.debug('Requests displayed:')
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
        if self.request.GET.get('reverse', ''):
            context['reversed'] = 1
        else:
            context['reversed'] = 0
        return context


class AjaxFormMixin(object):
    """ This class adds functionality to post forms via AJAX """

    def form_valid(self, form):
        """
        Method to call when a valid form is posted
        :param form: the form that is being submitted
        :return: http or json response
        """
        response = super(AjaxFormMixin, self).form_valid(form)
        LOGGER_DEBUG.debug(form.data)
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps(form.data),
                content_type='application/json'
            )
        else:
            return response

    def form_invalid(self, form):
        """
        Method to call when an invalid form is posted
        :param form: the form that is being submitted
        :return: http or json response
        """
        LOGGER_DEBUG.debug(form.errors)
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps(form.errors),
                content_type='application/json'
            )
        else:
            return response


class PersonUpdateView(LoginRequiredMixin, AjaxFormMixin, UpdateView):
    """
    The update page view for my application
    """
    model = Person
    template_name = 'personal_info/edit.html'
    form_class = PersonUpdateForm

    def dispatch(self, request, *args, **kwargs):
        """
        This method is used to log the request
        :param request: the request that comes in
        :param args: arguments
        :param kwargs: keyword arguments
        :return: base class dispatch() method
        """
        LOGGER_INFO.info(request.path)
        return super(PersonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Method to get UpdateView success url
        :return: the success url to go after update
        """
        return "%s?status_message=Modified successfully" % reverse('home')

    def get_object(self, queryset=None):
        """
        This method returns the first Person object in the db
        :return: returns the object to edit
        """
        return Person.objects.first()

    def post(self, request, *args, **kwargs):
        """
        This method catches the cancel_button on a posted form
        :param request: the request that comes in
        :param args: arguments
        :param kwargs: keyword arguments
        :return: redirect or base class post()
        """
        if request.POST.get('cancel_button'):
            if request.is_ajax():
                return HttpResponse(
                    json.dumps(
                        {
                            'url': '%s?status_message=Editing canceled' %
                            reverse('home')
                        }
                    ),
                    content_type='application/json'
                )
            return HttpResponseRedirect(
                '%s?status_message=Editing canceled' %
                reverse('home')
            )
        return super(PersonUpdateView, self).post(request, *args, **kwargs)
