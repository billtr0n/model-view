from django.db import models
from django.utils import six

class SeparatedValuesField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.delimiter= kwargs.pop('delimiter', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return value.split(self.delimiter)

    def get_prep_value(self, value):
        if not value:
            return
        return self.delimiter.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

         
