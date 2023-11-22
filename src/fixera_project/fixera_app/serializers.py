from rest_framework import serializers

from . import models


class Bug(serializers.ModelSerializer):
        class Meta:
            model = models.Bug
            fields = '__all__'
