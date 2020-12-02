from rest_framework import serializers

from .models import Dummy

class DummySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ('id','value')