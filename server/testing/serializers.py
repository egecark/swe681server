from rest_framework import serializers

from .models import *

class DummySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dummy
        fields = ['id','value']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id','word']

    def save(self):
#        word = self.validated_data['word']
#        id = self.validated_data['id']
        word = self.word
        id = self.id
        wordModel = Word(id=id, word=word)
#        if wordModel.full_clean():
#            wordModel.save()
#            return wordModel
#        else:
#            return False

        wordModel.save()
        return wordModel

class GameStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameState
        fields = ['id','board','turn','client1','client2','client3','client4','score_1','score_2','score_3','score_4']

class MatchmakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matchmaking
        fields = ['id', 'client1', 'client2', 'client3', 'client4', 'num_players']

    def save(self, client):
        num_players = self.validated_data['num_players']
        if num_players >4:
            raise serializers.ValidationError({'num_players': 'Max 4 players'})
        if num_players <=1:
            raise serializers.ValidationError({'num_players': 'Min 2 players'})
        matchmaking = Matchmaking(client1=client, num_players=num_players)
        matchmaking.save()
        return matchmaking
