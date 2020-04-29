# -*- coding: utf-8 -*-

import os
import boto3
import math
import requests
import json


from custom_modules import data


# TODO: CHECK IF HAS NAME, ELSE USERNAME
def get_username(token):
    print('Getting user account information from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}
    
    # REQUEST FOR USER ACCOUNT INFORMATION
    url = data.URL_LICHESS_API + data.URL_ACCOUNT
    req = requests.get(url = url, headers=hed)
    r = req.json()
    print(r)
    #    print(r['profile']['firstName'])
    #    return r['profile']['firstName']
    print(r['username'])
    return r['username']




def get_user_account(token):
    print('Getting user account information from Lichess.org')
    hed = {'Authorization': 'Bearer ' + token}
    
    # REQUEST FOR USER ACCOUNT INFORMATION
    r = requests.get(url = data.URL_LICHESS_API + data.URL_ACCOUNT, headers=hed)
    return r.json()

