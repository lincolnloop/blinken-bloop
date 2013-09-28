from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Div
from crispy_forms.bootstrap import FormActions
import floppyforms as forms

from . import models

TIME_FORMAT = '%H:%M %p'


class EventForm(forms.ModelForm):
    start = forms.SplitDateTimeField(
        input_time_formats=[TIME_FORMAT],
        widget=forms.SplitDateTimeWidget(time_format=TIME_FORMAT)
    )
    end = forms.SplitDateTimeField(
        input_time_formats=[TIME_FORMAT],
        widget=forms.SplitDateTimeWidget(time_format=TIME_FORMAT)
    )

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

    class Media:
        css = {
            'screen': (
                'vendor/pickadate/css/default.css',
                'vendor/pickadate/css/default.date.css',
                'vendor/pickadate/css/default.time.css'
            )
        }
        js = (
            'vendor/pickadate/js/picker.js',
            'vendor/pickadate/js/picker.date.js',
            'vendor/pickadate/js/picker.time.js',
            'vendor/pickadate/js/legacy.js',
        )
