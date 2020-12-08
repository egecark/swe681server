from django.contrib import admin
from .models import Dummy, Matchmaking, GameState, Move

admin.site.register(Dummy)
admin.site.register(Matchmaking)
admin.site.register(GameState)
admin.site.register(Move)


# Register your models here.
