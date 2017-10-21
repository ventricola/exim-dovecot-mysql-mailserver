from lib import validators
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import CharField

class FQDNField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid fully quaified domain name.'),
    }
    default_validators = [validators.validate_fqdn]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(FQDNField, self).clean(value)

