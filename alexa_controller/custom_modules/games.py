# -*- coding: utf-8 -*-

import os
import boto3
import math
import requests
import json
import io

import random
import datetime

import chess
import chess.pgn

from custom_modules import utils, data


SPEED_CORRESPONDENCE = "correspondence"
MAX_NUM_GAME_LIST = 3


# GETS SINGLE GAME INFORMATION BY ID
def get_game_by_id(token, game_id):
    
    #game_id = 'S27aJ3x6'
    print('Getting ongoing games from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
    print(hed)
    params = {'pgnInJson': 'false', 'opening': 'true'}
    print(params)
    
    url = data.URL_LICHESS_API + (data.URL_SINGLE_GAME).format(game_id)
    print(url)
    # REQUEST LIST OF ALL ACTIVE GAMES
    req = requests.get(url = url, headers=hed, params=params)
    print(req)
    print(req.content)
    game = req.json()
    print(game)
    
    return game


# RETURNS THE GAME OPENING OR RETURNS NONE IF GAME HASN'T STARTED
def get_game_opening(game):
    return game['opening']['name'] if 'opening' in game.keys() else None

# RETURNS THE GAME'S MOVES IN STRING FORMAT
def get_game_moves_string(game):
    return game['moves']

# RETURNS THE GAME'S MOVES IN LIST FORMAT
def get_game_moves_list(game):
    return game['moves'].split()

# RETURNS TRUE IF THE GAME HAS FINISHED
def get_game_finished(game):
    return game['status'] in ['mate', 'outoftime', 'draw', 'resign']

# RETURNS THE OPPONENT'S USERNAME
def get_opponent_username(game, username):
    return game['players']['white']['user']['name'] if (game['players']['black']['user']['name'] == username) else game['players']['black']['user']['name']

# RETURNS THE OPPONENT'S COLOR
def get_opponent_color(game, username):
    print('Getting opponent color...')
    opponent_color = 'black' if (game['players']['white']['user']['name'] == username) else 'white'
    print('opponent_color: ' + opponent_color)
    return opponent_color

# RETURNS THE PLAYER'S COLOR
def get_player_color(game, username):
    print('Getting player color...')
    player_color = 'black' if (game['players']['black']['user']['name'] == username) else 'white'
    print('player_color: ' + player_color)
    return player_color

# RETURNS THE COLOR OF THE PLAYER WHO WON THE GAME IF IT HAS FINISHED
def get_game_winner(game):
    return game['winner'] if get_game_finished(game) else None

# RETURNS TRUE IF THE PLAYER HAS WON THE GAME, FALSE IF HE LOST OR DREW, AND NONE IF THE GAME HASN'T FINISHED
def get_player_won(game, username):
    return None if not get_game_finished(game) else (not (game['status'] == 'draw' or game['winner'] == get_opponent_color(game, username)))
    #return game['winner'] == get_player_color(game, username) if (get_game_finished(game) and game['status'] != 'draw') else ()

# RETURNS THE OPPONENT'S RATING
def get_opponent_rating(game, username):
    return game['players'][get_opponent_color(game, username)]['rating']

# RETURNS THE OPPONENT'S RATING CHANGE AFTER GAME IS FINISHED
def get_opponent_rating_diff(game, username):
    return game['players'][get_opponent_color(game, username)]['ratingDiff'] if get_game_finished(game) else None

# RETURNS THE PLAYER'S RATING
def get_player_rating(game, username):
    return game['players'][get_player_color(game, username)]['rating']

# RETURNS THE PLAYER'S RATING CHANGE AFTER GAME IS FINISHED
def get_player_rating_diff(game, username):
    return game['players'][get_player_color(game, username)]['ratingDiff'] if get_game_finished(game) else None



# CHECK IF MOVE DESCRIBES SPECIFIC PIECE'S SOURCE POSITION (Ndb3)
def checks_source_square_conflict(move):
    columns = 'abcdefgh'
    rows = '12345678'
    possible_conflicts = [x+y for x in columns + rows for y in columns]
    for possible_conflict in possible_conflicts:
        if possible_conflict in move:
            return {'has_conflict': True, 'conflict': possible_conflict}
    return {'has_conflict': False, 'conflict': None}


# RETURNS A CLEAR WAY TO SAY THE MOVE
# EXAMPLE 1: dxe6 --> d takes on e5
# EXAMPLE 2: Nd5 --> Knight to d5
# EXAMPLE 3: a8=Q+ --> pawn to a8, promoting to queen with check
# EXAMPLE 4: bxc8=Q+ --> pawn b takes on c8, promoting to queen with check.
def get_move_speak(move):
    print('Getting move speak')
    # CHECKS IF IT IS A CASTELING MOVE OR A PIECE IS TAKEN
    taking_move = 'x' in move
    move_speak = data.CASTLES_QUEEN_SIDE if 'O-O-O' in move else (data.CASTLES_KING_SIDE if 'O-O' in move else move.replace('x', ' ' + data.TAKES_ON))
    
    # CHECKS IF MOVE HAS + OR # FOR CHECK AND CHECKMATE TO ADD TO RESPONSE STRING
    move_speak = move_speak.replace('+', data.WITH_CHECK).replace('#', data.WITH_CHECKMATE)
    
    # CHECKS IF THERE WAS A PROMOTION AND FORMATS STRING
    if '=' in move_speak:
        x = move_speak.find('=')
        promotion_piece_index = x + 1
        move_speak = move_speak.replace(move_speak[promotion_piece_index], data.PIECE_CODES[move_speak[promotion_piece_index]])
        move_speak = move_speak.replace('=', data.PROMOTING_PIECE)
    
    # CHECKS IF IT IS A PAWN MOVE OR A PIECE MOVE
    is_pawn_move = not ('K' in move_speak or 'Q' in move_speak or 'R' in move_speak or 'N' in move_speak or 'B' in move_speak)
    
    # CHECKS IF THERE ARE MULTIPLE POSSIBLE SOURCE SQUARES TO SPECIFY MOVE
    has_conflict = checks_source_square_conflict(move)

    # CHECKS IF IS A MOVE WITH A PAWN OR PIECE
    if is_pawn_move:
        move_speak = data.PAWN + (' ' if taking_move else ' to ') + move_speak
    else:
        # REPLACES THE PIECE CODE BY THE PIECE NAME
        for code, piece in data.PIECE_CODES.items():
            #move_speak = move_speak.replace(code, ' ' + piece)
            move_speak = move_speak.replace(code, ' ' + piece + ' ').replace(has_conflict['conflict'], has_conflict['conflict'][0] + ('' if taking_move else ' to ') + has_conflict['conflict'][1]) if has_conflict['conflict'] else move_speak.replace(code, ' ' + piece + ('' if taking_move else ' to '))

    return move_speak

# RETURNS THE LAST MOVE FROM A GAME MOVE STACK
def get_last_move(game):
    lastmove = (game['moves'].split()[-1]) if game['moves'] else ''
    return lastmove


# RETURNS IF IT IS THE PLAYER'S TURN
def is_player_turn(game, username):
    print('Checking if it is player turn...')
    
    if get_game_finished(game):
        print('Game has already finished...')
        return False
    elif not game['moves']:
        print('It is the game first move, so it is white to play...')
        return get_player_color(game, username) == 'white'
    else:
        pgn = io.StringIO(game['moves'])
        g = chess.pgn.read_game(pgn)
        board = g.board()
        for move in g.mainline_moves():
            board.push(move)
        print(board.turn)
        return ((board.turn == chess.WHITE) and get_player_color(game, username) == 'white') or ((board.turn == chess.BLACK) and get_player_color(game, username) == 'black')



# LISTS ALL ONGOING GAMES
def list_ongoing_games(token):
    print('Getting ongoing games from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}

    # REQUEST LIST OF ALL ACTIVE GAMES
    req = requests.get(url = data.URL_LICHESS_API + data.URL_ACTIVE_GAMES, headers=hed)
    print(req)
    r = req.json()
    print(r)
    
    return r['nowPlaying']
    
# PREPARES RESPONSE FORMAT WITH LISTS OF OPPONENTS
def get_ongoing_games_opponents_response(ongoing_games_dict):
    print('Preparing active games opponents response')
    ongoing_games_opponents_response = ''
    
    print(ongoing_games_dict)
    
    for key, game in ongoing_games_dict.items():
        if key < MAX_NUM_GAME_LIST + 1:
            print(game)
            ongoing_games_opponents_response += 'game {}, against '.format(key) + game['opponent']['username'] + (', ' if (key < len(ongoing_games_dict.items()) and key != MAX_NUM_GAME_LIST) else '. ')

    print(ongoing_games_opponents_response)
    return ongoing_games_opponents_response


# FORMATS THE LIST OF ONGOING GAMES TO DISPLAY TO USER
def get_ongoing_games_list(ongoing_games_dict):
    response = ''
    for key, game in ongoing_games_dict.items():
        response += (data.LIST_GAMES_ITEM).format(key, game['opponent']['username'], game['color']) + (data.LIST_GAMES_ITEM_PLAYER_TURN if game['isMyTurn'] else '') + '\n'
    return response


# TODO: TREAT CASES WITH 0 ACTIVE GAMES
def get_ongoing_games_response(ongoing_games):
    print('Building ongoing games response')
    ongoing_games_opponents_card_response = ''
    
    player_turn = 0
    
    active_correspondence_games = 0
    active_games_opponents = []
    
    ongoing_games_dict = {}
    
    for game in ongoing_games:
        if game['speed'] == SPEED_CORRESPONDENCE:
            active_correspondence_games += 1
            ongoing_games_dict[active_correspondence_games] = game
            player_turn += 1 if game['isMyTurn'] else 0


    ongoing_games_opponents_card_response = get_ongoing_games_list(ongoing_games_dict)
    ongoing_games_opponents_speak_response = (data.LIST_GAMES_NUMBER_OF_GAMES).format(active_correspondence_games, player_turn) + (data.LIST_GAMES_SOME_GAMES).format(get_ongoing_games_opponents_response(ongoing_games_dict)) + data.DETAILS_IN_SINGLE_GAME_QUESTION

    print(ongoing_games_opponents_speak_response)
    print(ongoing_games_opponents_card_response)


    return ongoing_games_opponents_speak_response, ongoing_games_opponents_card_response, ongoing_games_dict


# RETURNS THE CARD TITLE FOR THE GAME DETAILS
def get_game_details_card_title(game, username):
    return (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE).format(opponent=get_opponent_username(game, username), rating=get_opponent_rating(game, username))

# RETURNS THE SPEECH AND CARD RESPONSE FOR THE GAME DETAILS INTENT
def get_game_details_response(game, username):
    
    rsp_speak = (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_SPEAK).format(opponent=get_opponent_username(game, username), rating=get_opponent_rating(game, username), color=get_player_color(game, username)) + (data.DETAILS_IN_SINGLE_GAME_LAST_MOVE_SPEAK).format(move=get_move_speak(get_last_move(game))) + ((data.IS_USER_TURN + data.PLACE_A_MOVE_QUESTION) if is_player_turn(game, username) else (utils.get_random_string_from_list(data.DETAILS_IN_ANOTHER_GAME_QUESTION) + '\n\n'))
    
    rsp_card_content = (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_CONTENT).format(opening=get_game_opening(game), moves=get_game_moves_string(game))
    rsp_card_title = get_game_details_card_title(game, username)

    return rsp_speak, rsp_card_content, rsp_card_title


# PLACES A MOVE IN ACTIVE GAME
# TODO: RESIGN
# TODO: OFFER DRAW
def place_move(token, game_id, move):
    print('Placing move {} in game {}'.format(move, game_id))
    hed = {'Authorization': 'Bearer ' + token}
    
    url = data.URL_LICHESS_API + (data.URL_PLACE_MOVE).format(game_id, move)
    print(url)
    # sending get request and saving the response as response object
    r = (requests.post(url = url, headers=hed)).json()
    print(r)
    #data = r.json()
    #print(data)
    
    response = {}
    if r.get('ok'):
        ts = datetime.datetime.now().timestamp()
        rand = random.Random(int(ts))
        response = {'status': True, 'message': 'success', 'move': move}
        print(response)
        return response
    else:
        response = {'status': False, 'message': r.get('error'), 'move': move}
        print(response)
        return response


# GETS RESPONSE FOR THE PLACE MOVE INTENT
def get_place_move_response(move_dict):
    
    if move_dict['status']:
        move = move_dict['move']
        place_move_speak_response = (data.PLACE_MOVE_SUCCESS_SPEAK).format(move=get_move_speak(move)) + utils.get_random_string_from_list(data.DETAILS_IN_ANOTHER_GAME_QUESTION)
        place_move_card_response = (data.PLACE_MOVE_SUCCESS_CARD).format(move=move)
        return place_move_speak_response, place_move_card_response
    else:
        place_move_speak_response = (data.PLACE_MOVE_ERROR_SPEAK).format(move=get_move_speak(move)) + utils.get_random_string_from_list(data.DETAILS_IN_ANOTHER_GAME_QUESTION)
        place_move_card_response = (data.PLACE_MOVE_ERROR_CARD).format(move=move)
        return place_move_speak_response, place_move_card_response
