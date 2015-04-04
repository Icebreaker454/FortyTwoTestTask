"""
This module contains utility functions for my application
"""
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


def paginate(objects, size, request, context, var_name='object_list'):
    """
    This method paginates a given queryset
    :param objects: the queryset object to paginate
    :param size: size of the page
    :param request: the request from which the data comes
    :param context: context data to be modified
    :param var_name: desired context variable name
    :return: updated context object
    """

    paginator = Paginator(objects, size)

    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context
