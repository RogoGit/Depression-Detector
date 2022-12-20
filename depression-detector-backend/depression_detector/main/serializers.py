from rest_framework import serializers

from .models import Model


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ['url', 'text', 'date_of_birth', 'sex', 'depression_detection_result']
