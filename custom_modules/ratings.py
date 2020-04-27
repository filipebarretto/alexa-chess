# -*- coding: utf-8 -*-

import os
import boto3
import math

#s3 = boto3.client('s3')

# BOARD DEFAULTS


import requests
import json

import chess
import chess.svg
import cairosvg


s3 = boto3.client('s3')


CORRESPONDENCE = "correspondence"


MAX_NUM_GAME_LIST = 3

BOARD_IMAGES_BUCKET = "BOARD_IMAGES_BUCKET"

URL_ACTIVE_GAMES = "https://lichess.org/api/account/playing"

# https://lichess.org/api/board/game/{gameId}/move/{move}
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
    ongoing_games_opponents_speak_response = 'You have {} active correspondence games and it is your turn in {} of them. '.format(active_correspondence_games, player_turn) + ' Some of these games are ' + get_ongoing_games_opponents_response(ongoing_games_dict) + ' Would you like to get details in one of these games?'

    print(ongoing_games_opponents_speak_response)
    print(ongoing_games_opponents_card_response)


    return ongoing_games_opponents_speak_response, ongoing_games_opponents_card_response, ongoing_games_dict



def get_game_details_response(game):
    rsp = 'The game is against {}, who\'s raiting is {}, and you are playing with the {} pieces. '.format(game['opponent']['username'], game['opponent']['rating'], game['color']) + ('The last move was {}. '.format(game['lastMove']) if game['lastMove'] else '')

    return rsp, game['isMyTurn']


def place_move(token, game_id, move):
    print("Moving piece...")
    print('Getting ongoing games from Lichess.org')
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
        response = {'status': True, 'message': 'Move {} placed with success.  Would you like to view another game?'.format(move)}
        print(response)
        return response
    else:
        response = {'status': False, 'message': data.get('error')}
        print(response)
        return response


    

# GENERATES BOARD IMAGE
def get_board_image(game_id, fen, color, lastmove):
    print("Getting board image...")
    parts = fen.replace("_", " ").split(" ", 1)
    board = chess.BaseBoard("/".join(parts[0].split("/")[0:8]))
    
    size = min(max(int(360), 16), 1024)
    
    css = None
    lastmove = chess.Move.from_uci(lastmove) if lastmove else None
    check = None
    arrows = []
    
    flipped = (color == "black")
    
    svg_data = chess.svg.board(board, coordinates=False, flipped=flipped, lastmove=lastmove, check=check, arrows=arrows, size=size, style=css)
    png_data = cairosvg.svg2png(bytestring=svg_data)
    
    s3_bucket = os.environ[BOARD_IMAGES_BUCKET]
    obj_key = game_id + ".png"
    
    response = s3.put_object(Body=png_data, Bucket=s3_bucket, Key=obj_key)
    print(response)
    
    url = s3.generate_presigned_url("get_object", Params = {"Bucket": s3_bucket, "Key": obj_key}, ExpiresIn = 3600)
    print(url)
    
    return url


'''

def is_valid_move(b, m):
    print("Validating move...")
    move = chess.Move.from_uci(m)
    return(move in b.legal_moves)


def get_slots(slots):
    items = []
    resolved_slot = None
    for _, slot in six.iteritems(slots):
        print(slot)
        if slot.value is not None:
            resolved_slot = slot.value
            items.append(slot.value.lower())
    return items


def move_piece(b, m):
    print("Moving piece...")
    move = chess.Move.from_uci(m)
    print(b.san(move))
    b.push(move)
    return b

def get_move_san(b, m):
    move = chess.Move.from_uci(m)
    return(b.san(move))


# GENERATES BOARD IMAGE
def get_board_image(b):
    print("Getting board image...")
    fen = b.fen()
    parts = fen.replace("_", " ").split(" ", 1)
    board = chess.BaseBoard("/".join(parts[0].split("/")[0:8]))

    size = min(max(int(360), 16), 1024)

    css = None
    lastmove = None
    check = None
    arrows = []

    flipped = False

    svg_data = chess.svg.board(board, coordinates=False, flipped=flipped, lastmove=lastmove, check=check, arrows=arrows, size=size, style=css)
    png_data = cairosvg.svg2png(bytestring=svg_data)

    s3_bucket = "alexa-chess-images"
    obj_key = "test.png"
    
    s3.put_object(Body=png_data, Bucket=s3_bucket, Key=obj_key)
    
    url = s3.generate_presigned_url("get_object", Params = {"Bucket": s3_bucket, "Key": obj_key}, ExpiresIn = 3600)
    print(url)

    return url

'''
