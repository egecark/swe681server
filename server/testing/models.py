from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
import uuid


# Create your models here.
class Dummy(models.Model):
    value = models.CharField(max_length=60)
    def __str__(self):
        return self.value

class Move(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey('GameState', on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client', default=None, on_delete=models.CASCADE)
    move = models.CharField(max_length=20)

#Has the state of a game including the current board, whose turn it is, and player info
class GameState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    turn = models.CharField(max_length=20, default='game_not_started')
    board = models.CharField(max_length=5000)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='start_time')
    client1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client1_game', default=None, on_delete=models.CASCADE)
    client2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client2_game', default=None, on_delete=models.CASCADE)
    client3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client3_game', default=None, null= True, on_delete=models.CASCADE)
    client4 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client4_game', default=None, null= True, on_delete=models.CASCADE)
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(null=True, default=None)
    score_4 = models.IntegerField(null=True, default=None)
    bag = models.CharField(default=None, max_length=200)
    letters1 = models.CharField(default=None, max_length=20)
    letters2 = models.CharField(default=None, max_length=20)
    letters3 = models.CharField(null=True, default=None, max_length=20)
    letters4 = models.CharField(null=True, default=None, max_length=20)
    move1 = models.CharField(null=True, default=None, max_length=7)
    move2 = models.CharField(null=True, default=None, max_length=7)
    move3 = models.CharField(null=True, default=None, max_length=7)
    move4 = models.CharField(null=True, default=None, max_length=7)
    def __str__(self):
        return str(self.id)


#created when a user is waiting for a game and deleted when game is found
class Matchmaking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client1_match', default=None, on_delete=models.CASCADE)
    client2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client2_match', default=None, null=True, on_delete=models.CASCADE)
    client3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client3_match', default=None, null=True, on_delete=models.CASCADE)
    client4 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client4_match', default=None, null=True, on_delete=models.CASCADE)
    num_players = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(4),])
    def __str__(self):
        return str(self.id)

#Has the state of a game including the current board, whose turn it is, and player info
class Word(models.Model):
    id = models.UUIDField(primary_key=True)
    word = models.CharField(max_length=7)
    game_complete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + ' ' + str(self.word)
