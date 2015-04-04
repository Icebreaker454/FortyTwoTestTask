# -*- coding: utf-8 -*-

"""
    The models file for ticket1
"""
from PIL import ExifTags
from PIL import Image
import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

LOGGER_DEBUG = logging.getLogger('personal_info.debug')


@receiver(post_save)
def log_change_models_models(
        sender,
        **kwargs
):
    """
    The model change (create or update) signal processor
    :param sender: the model that sends the signal
    :param kwargs: keyword arguments
    :return: None
    """
    # Don't think it's a good idea to log changes from
    # the model that is used for logging model changes.
    # As with AJAX updating the requests page...
    if sender is not ModelLog:
        instance = kwargs['instance']
        try:
            model_id = instance.id
        except AttributeError:
            model_id = None
        if kwargs['created']:
            log = ModelLog(
                action='CREATE',
                model=sender.__name__,
                model_id=model_id
            )
        else:
            log = ModelLog(
                action='UPDATE',
                model=sender.__name__,
                model_id=model_id
            )
        LOGGER_DEBUG.debug(log.__unicode__())
        log.save()


@receiver(pre_delete)
def log_delete_models(sender, **kwargs):
    """
    The model delete signal processor
    :param sender: the model that sends the signal
    :param kwargs:
    :return: None
    """
    if sender is not ModelLog:
        instance = kwargs['instance']
        try:
            model_id = instance.id
        except AttributeError:
            model_id = None
        log = ModelLog(
            action='DELETE',
            model=sender.__name__,
            model_id=model_id
        )
        LOGGER_DEBUG.debug(log.__unicode__())
        log.save()

BASE_WIDTH = 200


class Person(models.Model):
    """ The Person model itself """

    class Meta:
        """ Class, that contains metadata for the model """
        verbose_name = u'Person'
        verbose_name_plural = u'Persons'

    first_name = models.CharField(
        max_length=128,
        blank=False,
    )
    last_name = models.CharField(
        max_length=128,
        blank=False,
    )
    birth_date = models.DateField(
        blank=False,
    )
    bio = models.TextField()
    contacts_email = models.EmailField(
        max_length=128,
        blank=False,
        verbose_name=u'Email'
    )
    contacts_jabber_id = models.EmailField(
        blank=True,
        verbose_name=u'Jabber JID'
    )
    contacts_skype_id = models.CharField(
        blank=True,
        max_length=32,
        verbose_name=u'Skype:'
    )
    contacts_other = models.TextField(
        blank=True,
        verbose_name=u'Other'
    )
    picture = models.ImageField(
        upload_to='pictures',
        blank=True,
        null=True
    )

    def get_admin_url(self):
        """
        This method returns the admin edit url for the model
        :return: the admin edit url for the model
        """
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            'admin:%s_%s_change' % (
                content_type.app_label,
                content_type.model
            ),
            args=(self.id,)
        )

    def __unicode__(self):
        """
        The method to represent model as a string
        :return: model's string representation
        """
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, force_insert=False, force_update=False, using=None):
        """ Method to scale all pictures to 200x200 """
        if self.picture:
            super(Person, self).save(force_insert, force_update)

            pw = self.picture.width
            ph = self.picture.height
            if (pw > 200) or (ph > 200):
                # We require a resize
                filename = str(self.picture.path)
                img = Image.open(filename)

                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                try:
                    exif = dict(img._getexif().items())

                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
                except AttributeError:
                    pass

                w_percent = (BASE_WIDTH/float(img.size[0]))
                h_size = int((float(img.size[1])*float(w_percent)))
                img = img.resize((BASE_WIDTH, h_size), Image.ANTIALIAS)
                img.save(filename)
        else:
            super(Person, self).save(force_insert, force_update)


class WebRequest(models.Model):
    """ The Request model for the Requests Page """

    time = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    get = models.TextField()
    post = models.TextField()
    remote_address = models.IPAddressField()
    method = models.CharField(max_length=7)
    priority = models.PositiveIntegerField(default=0)

    def get_admin_url(self):
        """
        This method returns the admin edit url for the model
        :return: the admin edit url for the model
        """
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            'admin:%s_%s_change' % (
                content_type.app_label,
                content_type.model
            ),
            args=(self.id,)
        )

    def __unicode__(self):
        """
        Method to convert Webrequest model to a string
        :return: WebRequest string representation
        """
        return "%s%s" % (self.remote_address, self.path)


class ModelLog(models.Model):
    """
    The model for the signal processor to store data
    about model creating, editing and deleting
    """
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete')
    )

    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(
        max_length=6,
        choices=ACTION_CHOICES
    )
    model = models.CharField(max_length=100)
    model_id = models.SmallIntegerField(
        null=True
    )

    def __unicode__(self):
        """
        The method to get the ModelLog string representation
        :return: the ModelLog string representation
        """
        return "%s: %s %s %s" % (
            self.date,
            self.model,
            self.model_id,
            self.action
        )
