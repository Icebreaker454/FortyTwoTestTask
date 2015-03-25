# -*- coding: utf-8 -*-

"""
    The models file for ticket1
"""
from django.db import models


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
        blank=False
    )
    contacts_jabber_id = models.EmailField()
    contacts_skype_id = models.CharField(
        max_length=32
    )
    contacts_other = models.TextField()

    def __unicode__(self):
        """
        The method to represent model as a string
        :return: model's string representation
        """
        return "%s %s" % (self.first_name, self.last_name)
