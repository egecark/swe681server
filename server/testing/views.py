
import random
import time
import enchant
import datetime

from scrabble import *
from testing.registrationForm import RegistrationForm
from testing.scrabbleForms import *
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import never_cache
from django.contrib.auth import login

from .serializers import *
from .models import *
from django.apps import apps

Accounts = apps.get_model('account', 'Account')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def get_available_matches(request):
    matches = Matchmaking.objects.all()
    serializer = MatchmakingSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def get_user_matches(request):
    matches = Matchmaking.objects.filter(Q(client1=request.user.id) |
                                         Q(client2=request.user.id) |
                                         Q(client3=request.user.id) |
                                         Q(client4=request.user.id))
    serializer = MatchmakingSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def get_user_games(request):
    games = GameState.objects.filter((Q(client1=request.user) |
                                     Q(client2=request.user) |
                                     Q(client3=request.user) |
                                     Q(client4=request.user)),
                                     active= True)
    serializer = GameStateSerializer(games, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@never_cache
def host_game(request):
    serializer = MatchmakingSerializer(data=request.data)
    data = {}
    if request.user.last_time_hosted:
        if (datetime.datetime.utcnow().replace(tzinfo=None) - request.user.last_time_hosted.replace(tzinfo=None)).total_seconds() > 30:
            if serializer.is_valid():
                request.user.last_time_hosted = datetime.datetime.utcnow()
                request.user.save()
                matchmaker = serializer.save(request.user)
                data['id'] = matchmaker.id
            else:
                return Response('Invalid hosting specifications')
            return Response(data)
        else:
            return HttpResponseBadRequest("You have to wait 30 seconds before hosting another game.")
    else:
        if serializer.is_valid():
            request.user.last_time_hosted = datetime.datetime.utcnow()
            request.user.save()
            matchmaker = serializer.save(request.user)
            data['id'] = matchmaker.id
        else:
            return Response('Invalid hosting specifications')
        return Response(data)

def start_game(client1, client2, client3, client4, caller):
    # build and save new gamestate
    game_state = GameState.objects.create(client1=client1,
                                          client2=client2,
                                          client3=client3,
                                          client4=client4,
                                          bag=[], letters1=[], letters2=[])
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
    turn = random.randrange(player_num) + 1
    game_state.turn = turn
    game_state.bag = ['E','E','E','E','E','E','E','E','E','E','E','E',
                      'A','A','A','A','A','A','A','A','A',
                      'I','I','I','I','I','I','I','I','I',
                      'O','O','O','O','O','O','O','O',
                      'N','N','N','N','N','N',
                      'R','R','R','R','R','R',
                      'T','T','T','T','T','T',
                      'L','L','L','L',
                      'S','S','S','S',
                      'U','U','U','U',
                      'D','D','D','D',
                      'G','G','G',
                      'B','B',
                      'C','C',
                      'M','M',
                      'P','P',
                      'F','F',
                      'H','H',
                      'V','V',
                      'W','W',
                      'Y','Y',
                      'K','J','X','Q','Z']
    for i in range(7):
        game_state.letters1.append(game_state.bag.pop(random.randrange(len(game_state.bag))))
        game_state.letters2.append(game_state.bag.pop(random.randrange(len(game_state.bag))))
        if player_num > 2:
            game_state.letters3.append(game_state.bag.pop(random.randrange(len(game_state.bag))))
        if player_num > 3:
            game_state.letters4.append(game_state.bag.pop(random.randrange(len(game_state.bag))))
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

    return response

@api_view(['GET'])
@never_cache
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def display_join_page(request):
    return render(request,
                  'matchmaking/matchmaking.html/',
                  {"hostform":MatchMakingHostingForm, "joinform":MatchMakingJoiningForm})


@api_view(['GET'])
@never_cache
@permission_classes([IsAuthenticated])
def get_moves(request):
    moves = Move.objects.filter(Q(is_game_ended=True)).order_by('game')
    response = {}
    for move in moves:
        response.update({str(move.id): {'move': move.move, 'username': move.client.username, 'game_id': move.game.id}})
    return Response(response)

@api_view(['GET'])
@never_cache
@permission_classes([IsAuthenticated])
def get_user_statistics(request):
    accounts = Accounts.objects.all() #.order_by('username')
    response = {}
    for account in accounts:
        response.update({str(account.id): {'username': account.username, 'win': account.win, 'lose': account.lose}})
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@never_cache
def join_game(request, matchmaking_id):
    user = request.user

    matches = Matchmaking.objects.filter(pk = matchmaking_id)

    if matches:
        matches = matches[0]

        if matches.client1 != user:
            if matches.client2 is None:
                matches.client2 = user
                if matches.num_players == 2:
                    response = start_game(matches.client1,
                                          matches.client2,
                                          None, None, user)
                    matches.delete()
                    return response

            elif matches.client3 is None:
                if matches.client2 == user:
                    return HttpResponse("You're already in the game")

                matches.client3 = user
                if matches.num_players == 3:
                    response = start_game(matches.client1,
                                          matches.client2,
                                          matches.client3,
                                          None, user)
                    matches.delete()
                    return response

            elif matches.client4 is None:
                if matches.client2 == user or matches.client3 == user:
                    return HttpResponse("You're already in the game")

                matches.client4 = user
                if matches.num_players == 4:
                    response = start_game(matches.client1,
                                          matches.client2,
                                          matches.client3,
                                          matches.client4,
                                          user)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def find_game(request):

    user_id = request.user

    if user_id.is_anonymous:
        return HttpResponse('you gotta authenticate')

    #check that request has client_id

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

            #send message to user from request
            #and wait for a response saying they're joining (timeout)

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
            game_state.board = [['3W','','','2L','','','','3W','','','','2L','','','3W'],
                                ['','2W','','','','3L','','','','3L','','','','2W',''],
                                ['','','2W','','','','2L','','2L','','','','2W','',''],
                                ['2L','','','2W','','','','2L','','','','2W','','','2L'],
                                ['','','','','2W','','','','','','2W','','','',''],
                                ['','3L','','','','3L','','','','3L','','','','3L',''],
                                ['','','2L','','','','2L','','2L','','','','2L','',''],
                                ['3W','','','2L','','','','X','','','','2L','','','3W'],
                                ['','','2L','','','','2L','','2L','','','','2L','',''],
                                ['','3L','','','','3L','','','','3L','','','','3L',''],
                                ['','','','','2W','','','','','','2W','','','',''],
                                ['2L','','','2W','','','','2L','','','','2W','','','2L'],
                                ['','','2W','','','','2L','','2L','','','','2W','',''],
                                ['','2W','','','','3L','','','','3L','','','','2W',''],
                                ['3W','','','2L','','','','3W','','','','2L','','','3W']]
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
@never_cache
def whose_turn_is_it(request, game_id):

    if request.method == 'GET':
        #request_data=json.loads(request.body)

        #Assumes a user can only be in 1 game
        game_state = GameState.objects.filter((Q(client1=request.user.id) |
                                               Q(client2=request.user.id) |
                                               Q(client3=request.user.id) |
                                               Q(client4=request.user.id))
                                              & Q(id=game_id))
        if game_state:
            game_state = game_state[0]

            if game_state.active:

                if (datetime.datetime.utcnow().replace(tzinfo=None) - game_state.last_move.replace(tzinfo=None)).total_seconds() > 3600:
                    moves = Move.objects.filter(Q(game=game_state))
                    if moves:
                        moves.update(is_game_ended=True)
                        for move in moves:
                            move.is_game_ended = True
                            move.save()

                    if game_state.turn == 1:
                        game_state.client1.lose = game_state.client1.lose + 1
                        game_state.client1.save()
                        game_state.client2.win = game_state.client2.win + 1
                        game_state.client2.save()

                        if game_state.client3:
                            game_state.client3.win = game_state.client3.win + 1
                            game_state.client3.save()
                        if game_state.client4:
                            game_state.client4.win = game_state.client4.win + 1
                            game_state.client4.save()

                    elif game_state.turn == 2:
                        game_state.client2.lose = game_state.client2.lose + 1
                        game_state.client2.save()

                        game_state.client1.win = game_state.client1.win + 1
                        game_state.client1.save()

                        if game_state.client3:
                            game_state.client3.win = game_state.client3.win + 1
                            game_state.client3.save()
                        if game_state.client4:
                            game_state.client4.win = game_state.client4.win + 1
                            game_state.client4.save()

                    elif game_state.turn == 3:
                        game_state.client3.lose = game_state.client3.lose + 1
                        game_state.client3.save()
                        game_state.client1.win = game_state.client1.win + 1
                        game_state.client1.save()

                        game_state.client2.win = game_state.client2.win + 1
                        game_state.client2.save()
                        if game_state.client4:
                            game_state.client4.win = game_state.client4.win + 1
                            game_state.client4.save()

                    elif game_state.turn == 4:
                        game_state.client4.lose = game_state.client4.lose + 1
                        game_state.client4.save()

                        game_state.client1.win = game_state.client1.win + 1
                        game_state.client1.save()

                        game_state.client2.win = game_state.client2.win + 1
                        game_state.client2.save()

                        game_state.client3.win = game_state.client3.win + 1
                        game_state.client3.save()

                    game_state.active = False
                    game_state.save()
                    return HttpResponseBadRequest("Time out")


                if request.user == game_state.client1:
                    player_letters = game_state.letters1
                elif request.user == game_state.client2:
                    player_letters = game_state.letters2
                elif request.user == game_state.client3:
                    player_letters = game_state.letters3
                elif request.user == game_state.client4:
                    player_letters = game_state.letters4
                else:
                    return HttpResponse("You are not in this game")

                game_over = False

                bag = game_state.bag

                player_out_of_letters = False


                if game_state.client1:
                    if not any(item in game_state.letters1 for item in letters):
                        player_out_of_letters = True

                if game_state.client2:
                    if not any(item in game_state.letters2 for item in letters):
                        player_out_of_letters = True

                if game_state.client3:
                    if not any(item in game_state.letters3 for item in letters):
                        player_out_of_letters = True

                if game_state.client4:
                    if not any(item in game_state.letters4 for item in letters):
                        player_out_of_letters = True

                if player_out_of_letters and not any(item in bag for item in letters):
                    game_over = True

                if game_over:
                    moves = Move.objects.filter(Q(game=game_state))
                    if moves:
                        for move in moves:
                            move.is_game_ended = True
                            move.save()

                    game_state.active = False
                    score1 = game_state.score_1
                    score2 = game_state.score_2
                    score3 = 0
                    score4 = 0
                    if game_state.client3:
                        score3 = game_state.score_3
                    if game_state.client4:
                        score4 = game_state.score_4

                    winner = 1

                    if score1 < score2:
                        winner = 2
                    if score2 < score3:
                        winner = 3
                    if score3 < score4:
                        winner = 4

                    if winner == 1:
                        game_state.client1.win = game_state.client1.win + 1
                        game_state.client1.save()
                        game_state.client2.lose = game_state.client2.lose + 1
                        game_state.client2.save()

                        if game_state.client3:
                            game_state.client3.lose = game_state.client3.lose + 1
                            game_state.client3.save()
                        if game_state.client4:
                            game_state.client4.lose = game_state.client4.lose + 1
                            game_state.client4.save()

                    elif winner == 2:
                        game_state.client2.win = game_state.client2.win + 1
                        game_state.client2.save()

                        game_state.client1.lose = game_state.client1.lose + 1
                        game_state.client1.save()

                        if game_state.client3:
                            game_state.client3.lose = game_state.client3.lose + 1
                            game_state.client3.save()
                        if game_state.client4:
                            game_state.client4.lose = game_state.client4.lose + 1
                            game_state.client4.save()

                    elif winner == 3:
                        game_state.client3.win = game_state.client3.win + 1
                        game_state.client3.save()
                        game_state.client1.lose = game_state.client1.lose + 1
                        game_state.client1.save()

                        game_state.client2.lose = game_state.client2.lose + 1
                        game_state.client2.save()
                        if game_state.client4:
                            game_state.client4.lose = game_state.client4.lose + 1
                            game_state.client4.save()

                    elif winner == 4:
                        game_state.client4.win = game_state.client4.win + 1
                        game_state.client4.save()

                        game_state.client1.lose = game_state.client1.lose + 1
                        game_state.client1.save()

                        game_state.client2.lose = game_state.client2.lose + 1
                        game_state.client2.save()

                        game_state.client3.lose = game_state.client3.lose + 1
                        game_state.client3.save()


                    game_state.save()
                    return HttpResponse('Game over')


                serializer = GameStateSerializer(game_state, many=False)
                response = {'player_letters': player_letters}
                response.update(serializer.data)
                return Response(response)
            else:
                return HttpResponseBadRequest("This game has ended")
        else:
            return HttpResponse("You are not in this game")



#function to handle user input. checks:
    #check if its actually that user's turn
    #check if that input is valid (regex)
    #check if its sorted (if not then sort here)
    #check if valid word position
    #check if user actually had all those letters
    #checks that all words involved are valid words
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@never_cache
def handle_input(request, game_id):

    #get the user id and check if its their turn
    if request.method == 'POST':
        data = request.data

        form = WordForm(data)

        if form.is_valid():
            wordModel = form.save()
        else:
            return HttpResponse('Invalid Move')


        word = wordModel.word
        game_id = wordModel.id

        if not word or not game_id:
            return HttpResponse('Invalid Move')

        #get game state with the requestor's client id
        game_state = GameState.objects.filter((Q(client1=request.user.id) |
                                               Q(client2=request.user.id) |
                                               Q(client3=request.user.id) |
                                               Q(client4=request.user.id))
                                              & Q(id=game_id))


        if game_state:
            game_state = game_state[0]
        else:
            return HttpResponse('Invalid Move')

        if game_state.active:

            if (datetime.datetime.utcnow().replace(tzinfo=None) - game_state.last_move.replace(tzinfo=None)).total_seconds() > 3600:
                moves = Move.objects.filter(Q(game=game_state))
                if moves:
                    moves.update(is_game_ended=True)
                    for move in moves:
                        move.is_game_ended = True
                        move.save()

                if game_state.turn == 1:
                    game_state.client1.lose = game_state.client1.lose + 1
                    game_state.client1.save()
                    game_state.client2.win = game_state.client2.win + 1
                    game_state.client2.save()

                    if game_state.client3:
                        game_state.client3.win = game_state.client3.win + 1
                        game_state.client3.save()
                    if game_state.client4:
                        game_state.client4.win = game_state.client4.win + 1
                        game_state.client4.save()

                elif game_state.turn == 2:
                    game_state.client2.lose = game_state.client2.lose + 1
                    game_state.client2.save()

                    game_state.client1.win = game_state.client1.win + 1
                    game_state.client1.save()

                    if game_state.client3:
                        game_state.client3.win = game_state.client3.win + 1
                        game_state.client3.save()
                    if game_state.client4:
                        game_state.client4.win = game_state.client4.win + 1
                        game_state.client4.save()

                elif game_state.turn == 3:
                    game_state.client3.lose = game_state.client3.lose + 1
                    game_state.client1.win = game_state.client1.win + 1
                    game_state.client1.save()

                    game_state.client2.win = game_state.client2.win + 1
                    game_state.client2.save()
                    if game_state.client4:
                        game_state.client4.win = game_state.client4.win + 1
                        game_state.client4.save()

                elif game_state.turn == 4:
                    game_state.client4.lose = game_state.client4.lose + 1
                    game_state.client4.save()

                    game_state.client1.win = game_state.client1.win + 1
                    game_state.client1.save()

                    game_state.client2.win = game_state.client2.win + 1
                    game_state.client2.save()

                    game_state.client3.win = game_state.client3.win + 1
                    game_state.client3.save()

                game_state.active = False
                game_state.save()
                return HttpResponseBadRequest("Time out")

            if game_state.client4:
                num_players = 4
            elif game_state.client3:
                num_players = 3
            else:
                num_players = 2


            #check user's letters
            player_letters = ''

            if game_state.client1 == request.user:
                if int(game_state.turn) != 1:
                    return Response('Invalid Move')
                player_letters = game_state.letters1
            elif game_state.client2 == request.user:
                if int(game_state.turn) != 2:
                    return Response('Invalid Move')
                player_letters = game_state.letters2
            elif game_state.client3 == request.user:
                if int(game_state.turn) != 3:
                    return Response('Invalid Move')
                player_letters = game_state.letters3
            elif game_state.client4 == request.user:
                if int(game_state.turn) != 4:
                    return Response('Invalid Move')
                player_letters = game_state.letters4

            player_letters = parse_string_array(player_letters)
            bag = parse_string_array(game_state.bag)
            test_word = word.split(',')

            valid_input = True
            letters_used = []

            input_rows = []
            input_cols = []

            temp_letters = player_letters

            for i in range(len(test_word)):
                if not valid_input:
                    break
                if i % 3 == 0: #should be a letter
                    if not test_word[i].capitalize() in letters: #if not a valid scrabble letter
                        valid_input = False
                        break

                    # if not in the current player's letters
                    elif not test_word[i].capitalize() in temp_letters:
                        valid_input = False
                        break

                    letters_used.append(test_word[i].capitalize())
                    temp_letters.remove(test_word[i].capitalize()) #remove letter from user's hand
                if i % 3 == 1: #should be a number (row)
                    if not test_word[i].isdigit(): #if its not an int
                        valid_input = False
                        break

                    # if the index would not fit on the board
                    elif int(test_word[i]) not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
                        valid_input = False
                        break
                    else:
                        input_rows.append(int(test_word[i]))

                if i % 3 == 2: #should be a number (col)
                    if not test_word[i].isdigit(): #if its not an int
                        valid_input = False
                        break

                    # if the index would not fit on the board
                    elif int(test_word[i]) not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
                        valid_input = False
                        break
                    else:
                        input_cols.append(int(test_word[i]))

            if not valid_input:
                return HttpResponse('Invalid Move')


            first_turn = True

            if game_state.score_1 or game_state.score_2 or game_state.score_3 or game_state.score_4:
                first_turn = False

            first_turn_check = True

            for i in range(len(input_rows)):
                if input_rows[i] == 7 and input_cols[i] == 7:
                    first_turn_check = False

            if first_turn_check and first_turn:
                valid_input = False

            if not valid_input:
                return HttpResponse('Invalid Move')

            board = game_state.board

            board, board_check = parse_board(board)

            #if false, couldnt parse board
            if not board_check:
                return HttpResponse('Invalid word')

            board, board_check = update_board(word, board)

            #if false, invalid word entered
            if not board_check:
                return HttpResponse('Invalid word')


            #calculate score function (calculates score of move,
            #returns score and list of connected words,
            #returns False if move had multiple rows and columns [invalid])
            word_score_with_connected_words = calculate(word, board)
            d = enchant.Dict("en_US")

            if not word_score_with_connected_words:
                return HttpResponse('Invalid word')


            valid_word = True

            connected_words = False
            main_word = []
            #if false, then the input word was not in a straight line (multiple columns and rows)
            if word_score_with_connected_words:
                word_score = word_score_with_connected_words[0]
                main_word = word_score_with_connected_words[1]
                connected_words = word_score_with_connected_words[2]
            else:
                valid_word = False

            try:
                #If no connected words found and its not the first move
                if not list(connected_words) and not first_turn and main_word == word:
                    valid_word = False
            except:
                pass


            #check if words are valid scrabble words
            word = ""
            for row in main_word:
                letter = row[0]
                word = word + letter.capitalize()

            if not d.check(str(word)):
                valid_word = False

            for connected in connected_words:
                word = ""
                for row in connected:
                    letter = row[0]
                    word = word + letter.capitalize()
                if not d.check(str(word)):
                    valid_word = False

            if not valid_word:
                serializer = GameStateSerializer(game_state)
                return HttpResponseBadRequest('not a valid move')
            else:
                if game_state.client1 == request.user:
                    game_state.score_1 += word_score
                    for ind in range(len(letters_used)):
                        if bag:
                            player_letters.append(bag.pop(random.randrange(len(bag))))
                    player_letters = [i for i in player_letters if i] #remove any empty strings
                    game_state.letters1 = player_letters
                    game_state.bag = bag
                elif game_state.client2 == request.user:
                    game_state.score_2 += word_score
                    for ind in range(len(letters_used)):
                        if bag:
                            player_letters.append(bag.pop(random.randrange(len(bag))))
                    player_letters = [i for i in player_letters if i] #remove any empty strings
                    game_state.letters2 = player_letters
                    game_state.bag = bag
                elif game_state.client3 == request.user:
                    game_state.score_3 += word_score
                    for ind in range(len(letters_used)):
                        if bag:
                            player_letters.append(bag.pop(random.randrange(len(bag))))
                    player_letters = [i for i in player_letters if i] #remove any empty strings
                    game_state.letters3 = player_letters
                    game_state.bag = bag
                elif game_state.client4 == request.user:
                    game_state.score_4 += word_score
                    for ind in range(len(letters_used)):
                        if bag:
                            player_letters.append(bag.pop(random.randrange(len(bag))))
                    player_letters = [i for i in player_letters if i] #remove any empty strings
                    game_state.letters4 = player_letters
                    game_state.bag = bag

                turn = int(game_state.turn)


                turn = turn + 1

                if turn > num_players:
                    if turn % num_players:
                        turn = turn % num_players
                    else:
                        turn = (turn % num_players) + num_players

                game_state.turn = turn

                game_state.board = str(board.tolist())
                game_state.last_move = datetime.datetime.utcnow().replace(tzinfo=None)
                game_state.save()
                serializer = GameStateSerializer(game_state)
                move = Move(game=game_state, client=request.user, move=test_word)
                move.save()


            return Response(serializer.data)
        else:
            return HttpResponseBadRequest("This game has ended")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def index(request):
    return render(request, 'game/index.html', {"form":WordForm})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def index_id(request, game_id):
    return render(request, 'game/index.html', {"form":WordForm})

@api_view(['GET'])
@permission_classes([])
@never_cache
def dashboard(request):
    return render(request, "game/dashboard.html")

@api_view(['GET', 'POST'])
@permission_classes([])
@never_cache
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

        return HttpResponseBadRequest("The info that you supplied, does not meet our registration criteria.")
