from django.urls import include, path
from rest_framework import routers
from .views import *

app_name = 'testing'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('dummy/', dummy_view, name="dummy"),
    path('host/', host_game, name="host"),
    path('matches/', get_available_matches, name="matches"),
    path('join/<matchmaking_id>/', join_game, name="join"),
    path('game/', index, name="index"),
    path('game/turn', whose_turn_is_it, name="turn"),
    path('game/findgame', find_game, name="findgame"),
    path('game/input', handle_input, name="input"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

