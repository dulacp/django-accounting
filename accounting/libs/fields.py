from django.db import models
import uuid


class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)

    def _generate_uuid(self):
        return str(uuid.uuid4())

    def pre_save(self, model_instance, add):
        if add or not getattr(model_instance, self.attname):
            value = self._generate_uuid()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)
