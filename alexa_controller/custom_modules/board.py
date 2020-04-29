# -*- coding: utf-8 -*-

import os
import boto3
import math
import requests
import json

import io
import chess
import chess.svg
import cairosvg

from custom_modules import data


s3 = boto3.client('s3')
BOARD_IMAGES_BUCKET = "BOARD_IMAGES_BUCKET"


#_details['id'], game_details['fen'], game_details['color'], game_details['lastMove']

# GENERATES BOARD IMAGE
def get_board_image(game, username):
    print("Getting board image...")
    
    '''
    parts = fen.replace("_", " ").split(" ", 1)
    board = chess.BaseBoard("/".join(parts[0].split("/")[0:8]))
    '''
    print('Generating board image...')
    pgn = io.StringIO(game['moves'])
    g = chess.pgn.read_game(pgn)
    print(g)
    board = g.board()
    for move in g.mainline_moves():
        board.push(move)

    print(board)
    #fen = board.fen()
    
    print('Getting white king square')
    white_king_square = board.king(chess.WHITE)
    print(white_king_square)
    print('Getting black attackers of white king square')
    white_king_attackers = board.attackers(chess.BLACK, white_king_square)
    print(white_king_attackers)
    
    print('Getting black king square')
    black_king_square = board.king(chess.BLACK)
    print(black_king_square)
    print('Getting white attackers of black king square')
    black_king_attackers = board.attackers(chess.WHITE, black_king_square)
    print(white_king_attackers)
    
    size = min(max(int(360), 16), 1024)
    
    css = None
    #lastmove = chess.Move.from_uci(lastmove) if lastmove else None
    lastmove = board.peek()
    print(lastmove)
    check = white_king_square if len(white_king_attackers) > 0 else (black_king_square if len(black_king_attackers) > 0 else None)
    arrows = []
    
    flipped = (game['players']['black']['user']['name'] == username)
    
    svg_data = chess.svg.board(board, coordinates=True, flipped=flipped, lastmove=lastmove, check=check, arrows=arrows, size=size, style=css)
    png_data = cairosvg.svg2png(bytestring=svg_data)
    
    s3_bucket = os.environ[BOARD_IMAGES_BUCKET]
    obj_key = game['id'] + ".png"
    
    response = s3.put_object(Body=png_data, Bucket=s3_bucket, Key=obj_key)
    print(response)
    
    url = s3.generate_presigned_url("get_object", Params = {"Bucket": s3_bucket, "Key": obj_key}, ExpiresIn = 3600)
    print(url)
    
    return url

