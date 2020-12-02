from rest_framework import serializers

from .models import *

class DummySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ['id','value']

class GameStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameState
        fields = ['id','game_id','board','turn','username1','username2','client_id1','client_id2','score1','score2']

class MatchmakingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matchmaking
        fields = ['id','client_id']
