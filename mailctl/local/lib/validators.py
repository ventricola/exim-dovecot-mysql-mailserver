import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.core import exceptions, validators
from django.core.validators import RegexValidator

class FQDNValidator(RegexValidator):

    def __call__(self, value):
        try:
            super(FQDNValidator, self).__call__(value)
        except ValidationError, e:
            raise

fqdn_re = re.compile(
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain
validate_fqdn = FQDNValidator(fqdn_re, _(u'Enter a valid fully qualified domain name.'), 'invalid')


