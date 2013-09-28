from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Div, HTML
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

    class Meta:
        model = models.Event
        widgets = {
            'max_attendees': forms.NumberInput,
            'max_guests': forms.NumberInput,
            'host': forms.HiddenInput
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

    def __init__(self, *args, **kwargs):
        show_actions = kwargs.pop('show_actions', None)
        render_form_tag = kwargs.pop('render_form_tag', True)
        super(EventForm, self).__init__(*args, **kwargs)

        actions = HTML('')
        if show_actions:
            actions = FormActions(
                Div(
                    HTML('<a href="{0}" class="btn btn-lg btn-block btn-link">'
                         'Nevermind</a>'.format(
                             reverse_lazy('events:dashboard'))),
                    css_class='col-xs-12 col-md-6'
                ),
                Div(
                    Submit('save', _('Create'),
                           css_class='primary btn-lg btn-block'),
                    css_class='col-xs-12 col-md-6'
                )
            )

        self.helper = FormHelper()
        self.helper.form_method = u'POST'
        self.helper.form_tag = render_form_tag
        self.helper.layout = Layout(
            Fieldset(
                u'',
                u'host',
                u'title',
                u'location',
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
            actions
        )
