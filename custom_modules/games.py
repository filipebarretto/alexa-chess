# -*- coding: utf-8 -*-

import os
import boto3
import math

#s3 = boto3.client('s3')

# BOARD DEFAULTS

import requests
import json


from custom_modules import data


s3 = boto3.client('s3')


CORRESPONDENCE = "correspondence"

MAX_NUM_GAME_LIST = 3

URL_ACTIVE_GAMES = "https://lichess.org/api/account/playing"
URL_PLACE_MOVE = "https://lichess.org/api/board/game/{}/move/{}"

def get_game_by_id(token, game_id):
    print('Getting ongoing games from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}
    
    r = requests.get(url = URL_ACTIVE_GAMES, headers=hed)
    print(r)
    data = r.json()
    print(data)
    
    for game in data['nowPlaying']:
        if game_id == game['gameId']:
            return game, data['nowPlaying']
    
    return None, data['nowPlaying']

def list_ongoing_games(token):
    print('Getting ongoing games from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}

    # sending get request and saving the response as response object
    r = requests.get(url = URL_ACTIVE_GAMES, headers=hed)
    print(r)
    data = r.json()
    print(data)
    
    return data['nowPlaying']
    

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


def get_ongoing_games_list(ongoing_games_dict):
    response = ''
    for key, game in ongoing_games_dict.items():
        response += '- Game {}, against {} ({})\n'.format(key, game['opponent']['username'], game['color'])
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
        if game['speed'] == CORRESPONDENCE:
            active_correspondence_games += 1
            ongoing_games_dict[active_correspondence_games] = game
            player_turn += 1 if game['isMyTurn'] else 0


    ongoing_games_opponents_card_response = get_ongoing_games_list(ongoing_games_dict)
    ongoing_games_opponents_speak_response = (data.LIST_GAMES_NUMBER_OF_GAMES).format(active_correspondence_games, player_turn) + (data.LIST_GAMES_SOME_GAMES).format(get_ongoing_games_opponents_response(ongoing_games_dict)) + data.DETAILS_IN_SINGLE_GAME_QUESTION

    print(ongoing_games_opponents_speak_response)
    print(ongoing_games_opponents_card_response)


    return ongoing_games_opponents_speak_response, ongoing_games_opponents_card_response, ongoing_games_dict



def get_game_details_response(game):
    rsp = (data.DETAILS_IN_SIGLE_GAME_OVERVIEW).format(game['opponent']['username'], game['opponent']['rating'], game['color']) + ((data.DETAILS_IN_SIGLE_GAME_LAST_MOVE).format(game['lastMove']) if game['lastMove'] else '')

    return rsp, game['isMyTurn']


def place_move(token, game_id, move):
    print('Placing move {} in game {}'.format(move, game_id))
    hed = {'Authorization': 'Bearer ' + token}
    
    url = URL_PLACE_MOVE.format(game_id, move)
    print(url)
    # sending get request and saving the response as response object
    r = requests.post(url = url, headers=hed)
    print(r)
    data = r.json()
    print(data)
    
    response = {}
    if data.get('ok'):
        response = {'status': True, 'message': (data.MOVE_PLACE_SUCCESS).format(move) + data.DETAILS_IN_ANOTHER_GAME_QUESTION}
        print(response)
        return response
    else:
        response = {'status': False, 'message': data.get('error')}
        print(response)
        return response



