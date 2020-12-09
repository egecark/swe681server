from django.urls import include, path
from rest_framework import routers
from .views import *

app_name = 'testing'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('dashboard/', dashboard, name="dashboard"),
#    path('finished_games/ids', get_ids_of_finished_games, name="ids"),
    path('moves/', get_moves, name="moves"),
    path('statistics/', get_user_statistics, name="statistics"),
    path('register/', register, name="register"),
    path('game/', index, name="game"),
    path('game/<game_id>/', index_id, name="game_id"),
    path('host/', host_game, name="host"),
    path('matches/', get_available_matches, name="matches"),
    path('user/matches/', get_user_matches, name="user_matches"),
    path('user/games/', get_user_games, name="user_games"),
    path('join/', display_join_page, name="join"),
    path('join/<matchmaking_id>/', join_game, name="join_id"),
    path('game/turn/<game_id>/', whose_turn_is_it, name="turn"),
    path('game/findgame/', find_game, name="findgame"),
    path('game/<game_id>/input/', handle_input, name="input"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
