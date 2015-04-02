import logging

from django import template
from django.db import models
from django.core.urlresolvers import reverse

register = template.Library()

LOGGER_INFO = logging.getLogger('personal_info.info')
LOGGER_DEBUG = logging.getLogger('personal_info.debug')


@register.tag(name='edit_link')
def edit_link(parser, token):
    """
    The compilation function for edit_link template tag
    :param parser: the template parser object
    :param token: the parameter object
    :return:
    """
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        LOGGER_INFO.info('edit_link : TemplateSyntaxException')
        raise template.TemplateSyntaxError(
            '%s tag requires exactly two arguments' %
            token.contents.split()[0]
        )
    if '"' in obj or "'" in obj:
        LOGGER_INFO.info('edit_link : TemplateSyntaxException')
        raise template.TemplateSyntaxError(
            "%s tag's argument shouldn't be in quotes" % tag_name
        )
    LOGGER_DEBUG.debug('edit_link processing object: {}'.format(obj))
    return EditLinkNode(obj)


class EditLinkNode(template.Node):
    """
    The node class for edit_link template tag
    """
    def __init__(self, editable_object):
        """
        The EditLinkNode initialization method
        """
        self.editable_object = template.Variable(editable_object)

    def render(self, context):
        """
        Method that renders the node
        :param context: the given context for rendering
        :return: rendered node
        """
        try:
            obj = self.editable_object.resolve(context)
            if isinstance(obj, models.Model):
                info = (obj._meta.app_label, obj._meta.module_name)
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

        except template.VariableDoesNotExist:
            LOGGER_INFO.info(
                'edit_link : VariableDoesNotExist'
            )
            return ''
