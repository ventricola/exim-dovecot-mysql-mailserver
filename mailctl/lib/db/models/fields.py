from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions, validators
from lib import validators
from lib import forms

class FQDNField(CharField):
    default_validators = [validators.validate_fqdn]
    description = _("Fully qualified domain name")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        CharField.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause email validation to be performed twice
        defaults = {
            'form_class': forms.FQDNField,
        }
        defaults.update(kwargs)
        return super(FQDNField, self).formfield(**defaults)

#add_introspection_rules([], ["^lib\.db\.models\.fields\.FQDNField"])
