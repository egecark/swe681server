from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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


#a find game request should include username/client_id which can be used to make a request if no available game request is found
@api_view(['GET'])
@permission_classes([])
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
@permission_classes([])
def whose_turn_is_it(request):

    if request.method == 'GET':
        #request_data=json.loads(request.body)

        #fix so that it finds gamestate by game_id and only sends if client_id of requestor matches
        game_state = GameState.objects.all()
        if game_state.exists():
            serializer = GameStateSerializer(game_state, many=False)


        else:
            return HttpResponse('game_not_started')
        return Response(serializer.data)

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
@permission_classes([])
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
    return render(request, 'index.html')
