from rest_framework import serializers

from .models import *

class DummySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ['id','value']

class GameStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameState
        fields = ['id','game_id','board','turn']

class MatchmakingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matchmaking
        fields = ='id','client_id']
