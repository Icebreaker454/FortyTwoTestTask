"""
    The personal_info admin module
"""
from django.contrib import admin

from apps.personal_info.models import Person
from apps.personal_info.models import WebRequest


class PersonAdmin(admin.ModelAdmin):
    """ Admin View for Person """
    fieldsets = (
        (
            'Personal Information', {
                'fields': (
                    'first_name',
                    'last_name',
                    'birth_date',
                    'bio'
                    )
            }
        ),
        (
            'Contacts', {
                'fields': (
                    'contacts_email',
                    'contacts_jabber_id',
                    'contacts_skype_id',
                    'contacts_other'
                    )
            }
        )
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(WebRequest)
