from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from testing.registrationForm import RegistrationForm
from testing.matchmakingForm import *
from random import randrange

import os
import time

from scrabble import *
import random
import json

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
@permission_classes([])
def dummy_view(request):
    dummy = Dummy.objects.all().order_by('value')
    serializer = DummySerializer(dummy, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_matches(request):
    matches = Matchmaking.objects.all()
    serializer = MatchmakingSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def host_game(request):
    serializer = MatchmakingSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        matchmaker = serializer.save(request.user)
        data['id'] = matchmaker.id
    else:
        data = serializer.errors
    return Response(data)


def start_game(client1, client2, client3, client4, caller):
    # build and save new gamestate
    game_state = GameState.objects.create(client1=client1, client2=client2, client3=client3, client4=client4, bag=[], letters1=[], letters2=[])
    player_num = 2
    if client4 is not None:
        player_num = 4
        game_state.score_3 = 0
        game_state.score_4 = 0
        game_state.letters3 = []
        game_state.letters4 = []
    elif client3 is not None:
        player_num = 3
        game_state.score_3 = 0
        game_state.letters3 = []
    turn = randrange(player_num + 1)
    game_state.turn = turn
    game_state.bag = ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A',
                      'I','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N',
                      'N','N','R','R','R','R','R','R','T','T','T','T','T','T','L','L','L','L','S','S','S',
                      'S','U','U','U','U','D','D','D','D','G','G','G','B','B','C','C','M','M','P','P','F',
                      'F','H','H','V','V','W','W','Y','Y','K','J','X','Q','Z','blank','blank']
    for i in range(7):
        game_state.letters1.append(game_state.bag.pop(randrange(len(game_state.bag))))
        game_state.letters2.append(game_state.bag.pop(randrange(len(game_state.bag))))
        if player_num > 2:
            game_state.letters3.append(game_state.bag.pop(randrange(len(game_state.bag))))
        if player_num > 3:
            game_state.letters4.append(game_state.bag.pop(randrange(len(game_state.bag))))
    player_letters = []
    if caller == client1:
        player_letters = game_state.letters1
    elif caller == client2:
        player_letters = game_state.letters2
    elif caller == client3:
        player_letters = game_state.letters3
    elif caller == client4:
        player_letters = game_state.letters4
    else:
        return HttpResponse("You cannot join this game!")
    game_state.board = [['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W'],
                        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
                        ['', '', '2W', '', '', '', '2L', '', '2L', '', '', '', '2W', '', ''],
                        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
                        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
                        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
                        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
                        ['3W', '', '', '2L', '', '', '', '', '', '', '', '2L', '', '', '3W'],
                        ['', '', '2L', '', '', '', '2L', '', '2L', '', '', '', '2L', '', ''],
                        ['', '3L', '', '', '', '3L', '', '', '', '3L', '', '', '', '3L', ''],
                        ['', '', '', '', '2W', '', '', '', '', '', '2W', '', '', '', ''],
                        ['2L', '', '', '2W', '', '', '', '2L', '', '', '', '2W', '', '', '2L'],
                        ['', '', '2W', '', '', '', '2L', '', '2L', '', '', '', '2W', '', ''],
                        ['', '2W', '', '', '', '3L', '', '', '', '3L', '', '', '', '2W', ''],
                        ['3W', '', '', '2L', '', '', '', '3W', '', '', '', '2L', '', '', '3W']]
    game_state.save()

    serializer = GameStateSerializer(game_state, many=False)
    response = Response(serializer.data)
    response['player_letters'] = player_letters

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def display_join_page(request):
    return render(request, 'matchmaking/matchmaking.html/', {"hostform":MatchMakingHostingForm, "joinform":MatchMakingJoiningForm})

api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def join_game(request, matchmaking_id):
    user = request.user

    matches = Matchmaking.objects.filter(pk = matchmaking_id)

    if matches:
        matches = matches[0]

        if matches.client1 != user:
            if matches.client2 is None:
                matches.client2 = user
                if matches.num_players == 2:
                    response = start_game(matches.client1, matches.client2, None, None, user)
                    matches.delete()
                    return response

            elif matches.client3 is None:
                if matches.client2 == user:
                    return HttpResponse("You're already in the game")

                matches.client3 = user
                if matches.num_players == 3:
                    response = start_game(matches.client1, matches.client2, matches.client3, None, user)
                    matches.delete()
                    return response

            elif matches.client4 is None:
                if matches.client2 == user or matches.client3 == user:
                    return HttpResponse("You're already in the game")

                matches.client4 = user
                if matches.num_players == 4:
                    response = start_game(matches.client1, matches.client2, matches.client3, matches.client4, user)
                    matches.delete()
                    return response
            matches.save()
            serializer = MatchmakingSerializer(matches, many=False)
            return Response(serializer.data)
        else:
            return HttpResponse("You're already in the game")
    # if no match waiting, make your own
    else:
        return HttpResponse("Invalid match id")

#a find game request should include username/client_id which can be used to make a request if no available game request is found
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_game(request):

    print('find game request')

    ##request_data = json.loads(request.body)

    user_id = request.user

    if user_id.is_anonymous:
        print('non authenticated user attempted access')
        return HttpResponse('you gotta authenticate')

    print('user id!!!')
    print(user_id)

    #check that request has client_id

    ##GameState.objects.create(game_id='1', turn='user1', board = [['3W','','','2L','','','','3W','','','','2L','','','3W'],['','2W','','','','3L','','','','3L','','','','2W',''],['','','2W','','','','2L','','2L','','','','2W','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','','','2W','','','','','','2W','','','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','2L','','','','2L','','2L','','','','2L','',''],['3W','','','2L','','','','X','','','','2L','','','3W'],['','','2L','','','','2L','','2L','','','','2L','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','','','2W','','','','','','2W','','','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','2W','','','','2L','','2L','','','','2W','',''],['','2W','','','','3L','','','','3L','','','','2W',''],['3W','','','2L','','','','3W','','','','2L','','','3W']])

    ##serializer = GameStateSerializer(GameState.objects.filter()[:1].get(), many=False)

    ##return Response(serializer.data)

    if request.method == 'GET':
        matches = Matchmaking.objects.first()

        if matches:

            #size check for client ids (add regex)
            if len(matches.values('client_id')) > 20:
                return False
            if len(user_id) > 20:
                return False

            client_id1 = matches.values('client_id')
            client_id2 = user_id

            #if client ids match then its that user's request so do nothing
            if client_id1 == client_id2:
                return HttpResponse('waiting_for_game')

            #size check for usernames (add regex)
            #if len(username1_from_server) > 20:
            #    return False
            #if len(username2_from_server) > 20:
            #    return False

            #get username from client_id
            username1 = 'find_their_actual_username'
            username2 = 'find_their_actual_username2'

            current_time = time.time()

            #send message to user from request and wait for a response saying they're joining (timeout)

            #if other user joining, then make gamestate

            #find unused game_id from server

            #randomly choose who goes first
            random_turn = random.getrandbits(1)

            if random_turn:
                turn = username1
            else:
                turn = username2

            #build and save new gamestate
            game_state = GameState.objects.create()
            game_state.game_id=-1
            game_state.client_id1=client_id1
            game_state.client_id2=client_id2
            game_state.turn=turn
            game_state.board = [['3W','','','2L','','','','3W','','','','2L','','','3W'],['','2W','','','','3L','','','','3L','','','','2W',''],['','','2W','','','','2L','','2L','','','','2W','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','','','2W','','','','','','2W','','','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','2L','','','','2L','','2L','','','','2L','',''],['3W','','','2L','','','','X','','','','2L','','','3W'],['','','2L','','','','2L','','2L','','','','2L','',''],['','3L','','','','3L','','','','3L','','','','3L',''],['','','','','2W','','','','','','2W','','','',''],['2L','','','2W','','','','2L','','','','2W','','','2L'],['','','2W','','','','2L','','2L','','','','2W','',''],['','2W','','','','3L','','','','3L','','','','2W',''],['3W','','','2L','','','','3W','','','','2L','','','3W']]
            game_state.save()

            serializer = GameStateSerializer(game_state, many=False)

            #delete match request
            matches.delete()

            return Response(serializer.data)

        #if no match waiting, make your own
        else:
            match = Matchmaking.objects.create()
            match.client_id = user_id
            match.save()
            serializer = MatchmakingSerializer(match, many=False)

            return Response(serializer.data)


#function to control turn changes. responds to get request.
#send score, board state
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whose_turn_is_it(request):

    if request.method == 'GET':
        #request_data=json.loads(request.body)

        #Assumes a user can only be in 1 game
        game_state = GameState.objects.filter(client1=request.user)
        if game_state:
            game_state = game_state[0]
            serializer = GameStateSerializer(game_state, many=False)
            return Response(serializer.data)


        else:
            return HttpResponse('game_not_started')


#function to handle user input. Should:
    #check if its actually that user's turn
    #check if that input is valid (regex)
    #check if its sorted (if not then sort here)
    #check if valid word position
    #check if user actually had all those letters
    #calculate score function
        #calculate score function should check that all words are valid scrabble words
#return serialized response telling if valid move.
    #If not then send board state to revert to.
    #if good then send list of tiles that user should have
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_input(request):

    #get the user id and check if its their turn

    if request.method == 'POST':
        request_data=json.loads(request.body)

        #probably change to httpresponse saying please send data
        if not request_data:
            serializer = GameStateSerializer([])
            return Response(serializer.data)

        #regex the input

        #doesn't filter for if a client has multiple games
        #get game state with the requestor's client id
        game_state = GameState.objects.filter(Q(client_id1=request_data.user.id) | Q(client_id2=request_data.user.id))

        word = request_data["word"]
        #sort the input word just in case

        #check for valid word position

        #check user's letters

        board = getattr(game_state, 'board')

        #calculate score function
        word_score = calculate(word, board)


        if not word_score:
            serializer = GameStateSerializer(game_state)
        else:
            if game_state.client_id1 == request_data.user.id:
                game_state.score1 += word_score
            elif game_state.client_id2 == request_data.user.id:
                game_state.score2 += word_score
            else:
                return HttpResponse('cannot find game')

            print(board)
            update_board(word, board) #need to make this function

            serializer = GameStateSerializer(game_state)


        return Response(serializer.data)


def index(request):
    return render(request, 'game/index.html')

def dashboard(request):
    return render(request, "game/dashboard.html")

def register(request):

    if request.method == "GET":

        return render(request, "registration/register.html", {"form": RegistrationForm})

    elif request.method == "POST":

        #form = UserCreationForm(request.POST)
        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("https://swe681project.com/dashboard/")

        else:
            return HttpResponse(form.is_valid())
