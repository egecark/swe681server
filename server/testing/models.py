from django.db import models

# Create your models here.
class Dummy(models.Model):
    value = models.CharField(max_length=60)
    def __str__(self):
        return self.value

#Has the state of a game including the current board, whose turn it is, and player info
class GameState(models.Model):
    game_id = models.CharField(max_length=20)
    turn = models.CharField(max_length=20, default='game_not_started')
    board = models.JSONField()
    client_id1 = models.CharField(max_length=20)
    client_id2 = models.CharField(max_length=20)
    username1 = models.CharField(max_length=20)
    username2 = models.CharField(max_length=20)
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    def __str__(self):
        return self.game_id

#created when a user is waiting for a game and deleted when game is found
class Matchmaking(models.Model):
    client_id = models.CharField(max_length=20)
    def __str__(self):
        return self.client_id

#ToDo: add a model for tiles (the bag contents and each player's) with a matching game_id

#GameState.objects.create(turn='game_not_started', board = [['3W','','','2L','','','','3W','','','','2L','','','3W'],['','2W','','','','3L','','','','3L','','','','2W',''],['','','2W','','','','2L','','2L','','','','2W','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','','','2W','','','','','','2W','','','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','2L','','','','2L','','2L','','','','2L','',''],['3W','','','2L','','','','X','','','','2L','','','3W'],['','','2L','','','','2L','','2L','','','','2L','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','','','2W','','','','','','2W','','','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','2W','','','','2L','','2L','','','','2W','',''],['','2W','','','','3L','','','','3L','','','','2W',''],['3W','','','2L','','','','3W','','','','2L','','','3W']])
