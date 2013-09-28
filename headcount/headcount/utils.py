from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext, loader


def generate_email(prefix, request, context=None, to=None, only_text=False):
    if not isinstance(to, (list, tuple)):
        raise ValueError(u"The `to` argument must be a list or tuple.")
    subject_template = loader.get_template(u'{0}_subject.txt'.format(prefix))
    text_template = loader.get_template(u'{0}.txt'.format(prefix))
    html_template = loader.get_template(u'{0}.html'.format(prefix))
    rc = RequestContext(request, context or {})
    subject = subject_template.render(rc)
    text = text_template.render(rc)
    rc.update({'subject': subject})
    html = html_template.render(rc)

    email = EmailMultiAlternatives(subject.strip(), text, to=to)

    if not only_text:
        email.attach_alternative(html, u"text/html")

    return email
