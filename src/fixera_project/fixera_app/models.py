from django.db import models


class Bug(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def __str__(self):
        return self.title
