# -*- coding: utf-8 -*-

"""
    The models file for ticket1
"""
from PIL import ExifTags
from PIL import Image

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
                img = img.resize((200, 200), Image.ANTIALIAS)
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

    def __unicode__(self):
        """
        Method to convert Webrequest model to a string
        :return: WebRequest string representation
        """
        return "%s%s" % (self.remote_address, self.path)
