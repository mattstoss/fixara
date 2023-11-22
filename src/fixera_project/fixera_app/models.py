from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True

    class SerializedManager(models.Manager):
        @staticmethod
        def _object_instance_to_dict(instance):
            attributes = dir(instance)
            result = {}
            for attr_name in attributes:
                if attr_name.startswith("_"):
                    continue
                if attr_name == 'objects':
                    continue
                attr_val = getattr(instance, attr_name)
                if callable(attr_val):
                    continue
                result[attr_name] = attr_val
            return result

        def all(self):
            objects = super().get_queryset().all()
            serialized_objects = [self._object_instance_to_dict(o) for o in objects]
            return serialized_objects

    objects = SerializedManager()


class Bug(BaseModel):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def list_all(cls):
        return cls.objects.all()

    def serialize_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
        }

    def __str__(self):
        return self.title
