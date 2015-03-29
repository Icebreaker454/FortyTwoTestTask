"""
    This module contains Model forms (e.g) Django-widgets
    for my application
"""
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.bootstrap import Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout

from apps.personal_info.models import Person


class LogInForm(AuthenticationForm):
    """ The model form for user logging in """
    def __init__(self, *args, **kwargs):
        """ Model form initalization method"""
        super(LogInForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'login-form active'
        self.helper.form_action = reverse('login')
        self.helper.form_method = 'POST'

        self.helper.help_text_inline = True
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Div(
                'username',
                'password'
            ),
            Div(
                Submit('login', 'Log in', css_class='btn btn-link')
            )
        )


class PersonUpdateForm(ModelForm):
    """ The model form for updating Person model """
    class Meta:
        """ Metadata for the modelform """
        model = Person

    def __init__(self, *args, **kwargs):
        """ Model form initialization method """
        super(PersonUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('update')
        self.helper.form_method = 'POST'

        self.helper.help_text_inline = True
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML("<h2 id='personal-info'>Personal Information</h2>"),
                    'first_name',
                    'last_name',
                    'birth_date',
                    'bio',
                    css_class='col-xs-6'
                ),
                Div(
                    HTML("<h2 id='contacts'>Contacts</h2>"),
                    'contacts_email',
                    'contacts_jabber_id',
                    'contacts_skype_id',
                    'contacts_other',
                    css_class='col-xs-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Submit('done_button', 'Save', css_class='btn btn-link'),
                    css_class='col-xs-12'
                ),
                css_class='row'
            )
        )
