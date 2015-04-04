"""
    This module contains Model forms (e.g) Django-widgets
    for my application
"""
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.bootstrap import Div
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout

from apps.personal_info.models import Person


class LogInForm(AuthenticationForm):
    """ The model form for user logging in """
    def __init__(self, *args, **kwargs):
        """ Model form initialization method"""
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
                    'picture',
                    Div(
                        HTML('<img {%if form.instance.picture %}src="\
                        {{form.instance.picture.url}}" {% endif %}\
                        id="preview" width="200"\
                        class="img img-rounded">'),
                    ),
                    Div(
                        HTML(
                            '<div class="row" id="loading-indicator"\
                                style="display: none">\
                              <div class="alert \
                                        alert-success" id="alert">\
                                <div class="spinner" style="display: none">\
                                  <div class="rect1"></div>\
                                  <div class="rect2"></div>\
                                  <div class="rect3"></div>\
                                  <div class="rect4"></div>\
                                  <div class="rect5"></div>\
                                </div>\
                              </div>\
                            </div>'
                        )
                    ),
                    FormActions(
                        Submit(
                            'done_button',
                            'Save',
                            css_class='btn btn-primary'
                        ),
                        Submit(
                            'cancel_button',
                            'Cancel',
                            css_class='btn btn-link'
                        ),
                    ),
                    css_class='col-xs-6'
                ),
                Div(
                    HTML("<h2 id='contacts'>Contacts</h2>"),
                    'contacts_email',
                    'contacts_jabber_id',
                    'contacts_skype_id',
                    'contacts_other',
                    'bio',
                    css_class='col-xs-6'
                ),
                css_class='row'
            ),

        )
