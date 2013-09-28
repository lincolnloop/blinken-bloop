from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Div
from crispy_forms.bootstrap import FormActions
import floppyforms as forms

from . import models


class EventForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            u'',
            u'title',
            u'description',
            Div(
                Div(u'start', css_class=u'col-xs-12 col-md-6'),
                Div(u'end', css_class=u'col-xs-12 col-md-6'),
                css_class=u'row'
            ),
            Div(
                Div(u'max_attendees', css_class=u'col-xs-12 col-md-6'),
                Div(u'max_guests', css_class=u'col-xs-12 col-md-6'),
                css_class=u'row'
            ),
            u'cost'
        ),
        Fieldset(
            _('Location'),
            u'venue_name',
            Div(
                Div(u'address', css_class=u'col-xs-12 col-md-6'),
                Div(u'address2', css_class=u'col-xs-12 col-md-6'),
                css_class=u'row'
            ),
            Div(
                Div(u'city', css_class=u'col-xs-12 col-md-4'),
                Div(u'state', css_class=u'col-xs-12 col-md-4'),
                Div(u'country', css_class=u'col-xs-12 col-md-4'),
                css_class=u'row'
            ),
        ),
        FormActions(
            Submit('save', _('Create your event'), css_class=u'primary')
        )
    )

    class Meta:
        model = models.Event
        widgets = {
            'start': forms.DateTimeInput,
            'end': forms.DateTimeInput,
            'max_attendees': forms.NumberInput,
            'max_guests': forms.NumberInput,
        }
