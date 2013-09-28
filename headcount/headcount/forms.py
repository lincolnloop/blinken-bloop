from django.utils.translation import ugettext_lazy as _

from authtools.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions


class HeadcountUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        show_actions = kwargs.pop('show_actions', True)
        render_form_tag = kwargs.pop('render_form_tag', True)
        super(HeadcountUserCreationForm, self).__init__(*args, **kwargs)

        actions = HTML('')
        if show_actions:
            actions = FormActions(
                Submit('save', _('Create'),
                       css_class='primary btn-lg btn-block'),
            )

        self.helper = FormHelper()
        self.helper.form_tag = render_form_tag
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            'name',
            'email',
            Div(
                Div(u'password1', css_class=u'col-xs-12 col-md-6'),
                Div(u'password2', css_class=u'col-xs-12 col-md-6'),
                css_class=u'row'
            ),
            actions
        )
