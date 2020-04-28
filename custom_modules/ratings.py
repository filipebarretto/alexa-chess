# -*- coding: utf-8 -*-

import os
import boto3
import math
import requests
import json
import random
import datetime


from custom_modules import data



def get_user_ratings(token):
    print('Getting user rating information from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}
    
    resp_speak = data.USER_RATINGS_INTRO
    resp_card = ''
    
    # REQUEST FOR USER ACCOUNT INFORMATION
    url = data.URL_LICHESS_API + data.URL_ACCOUNT
    req = requests.get(url = url, headers=hed)
    r = req.json()
    
    perfs = r['perfs']
    
    # LOOP THROUGH PERFS TO GET RATING AND NUMBER OF GAMES
    for k, v in perfs.items():
        if v['games'] > 1:
            resp_speak += (data.USER_RATINGS_ITEM_SPEAK).format(v['rating'], v['games'], k) + '<break time="0.5s"/>'
            resp_card += (data.USER_RATINGS_ITEM_CARD).format(k, v['rating'], v['games'])
    
    return resp_speak, resp_card



def get_user_ratings_in_speed(token, game_speed):
    print('Getting user rating in speed {} information from Lichess.org'.format(game_speed))
    hed = {'Authorization': 'Bearer ' + token}
    
    resp_speak = ''
    resp_card = ''
    
    ts = datetime.datetime.now().timestamp()
    rand = random.Random(int(ts))
    
    # REQUEST FOR USER ACCOUNT INFORMATION
    url = data.URL_LICHESS_API + data.URL_ACCOUNT
    req = requests.get(url = url, headers=hed)
    r = req.json()
    perfs = r['perfs']
    
    # LOOP THROUGH PERFS TO GET RATING AND NUMBER OF GAMES
    for k, v in perfs.items():
        if k == game_speed:
            resp_speak += (rand.choice(data.RATING_IN_SPEED_SPEAK)).format(speed=k, rating=v['rating'], games=v['games'])
            resp_card += (data.RATING_IN_SPEED_CARD).format(k, v['rating'], v['games'])

    print(resp_speak)
    return resp_speak, resp_card
