import logging

from django import template
from django.db import models
from django.core.urlresolvers import reverse

register = template.Library()

LOGGER_INFO = logging.getLogger('personal_info.info')
LOGGER_DEBUG = logging.getLogger('personal_info.debug')


@register.simple_tag()
def edit_link(editable_object):
    """
    The template tag that renders the admin edit link to a
    given object
    :param editable_object: the object to render it's link
    :return: rendered link
    """

    obj = editable_object
    if isinstance(obj, models.Model):
        info = (obj._meta.app_label, obj._meta.module_name)
        LOGGER_DEBUG.debug(
            'edit_link processing object: {}'.format(
                obj.__unicode__()
            )
        )
        return '<a href="{}">(Edit {} at Admin)</a'.format(
            reverse(
                'admin:%s_%s_change' % info,
                args=(obj.pk,),

            ),
            type(obj).__name__
        )
    else:
        LOGGER_INFO.info(
            'edit_link : TypeError, {}'.format(
                "object should be a model instance"
            )
        )
        return ''
