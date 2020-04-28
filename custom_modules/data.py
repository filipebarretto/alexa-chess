# -*- coding: utf-8 -*-

import random

URL_LICHESS_API = 'https://lichess.org/api/'
URL_ACTIVE_GAMES = 'account/playing'
URL_PLACE_MOVE = 'board/game/{}/move/{}'
URL_ACCOUNT = 'account'


WELCOME_MESSAGE = ("Hello, {}! Welcome to Alexa Chess. Here, you can play games on Lichess.org. What would you like to do?")
CHOOSE_ACTION = ["What would you like to do?", "How can I help you?"]
HELP_MESSAGE = ("How can I help you? ")
EXIT_SKILL_MESSAGE = ("Ok! See you later.")
FALLBACK_ANSWER = "Sorry, I didn't understand. Could you repeat? "
OK = "Ok! "

USER_RATINGS_CARD_TITLE = "Ratings"
USER_RATINGS_INTRO = "Your ratings are "
USER_RATINGS_ITEM_SPEAK = "{} in {} games in {}, "
USER_RATINGS_ITEM_CARD = "{}: {} in {} games\n"

RATING_IN_SPEED_SPEAK = ["Your rating in {speed} is {rating} in {games} games. ", "You have a {rating} rating in {games} {speed} games. ", "You have a rating of {rating} in {games} {speed} games. "]
RATING_IN_SPEED_CARD_TITLE = "Ratings in {}"
RATING_IN_SPEED_CARD = "{}: {} in {} games\n"

USER_RATINGS_TITLE = "User Ratings"

# ERROR MESSAGES
ERROR_MESSAGE = ("We had a problem. Please try again later. ")
ERROR_ACCESS_TOKEN = "Error retrieving access token"
ERROR_ACCESS_TOKEN_SPEAK = random.choice(["We had an error retrieving your access token.", "Error retrieving access token"])


MOVE_PIECE_RESPONSE = "Moving piece {} to {}."
ILEGAL_MOVE = "Illegal move. Place a different one."

ONGOING_GAMES_CARD_TITLE = "Ongoing Games"
GAME_DETAILS_CARD_TITLE = "Game against {}"


LIST_GAMES_NUMBER_OF_GAMES = "You have {} active correspondence games and it is your turn in {} of them. "
LIST_GAMES_SOME_GAMES = " Some of these games are {}"
LIST_GAMES_ITEM = "- Game {}, against {} ({}) "
LIST_GAMES_ITEM_PLAYER_TURN = "(Your turn)"

DETAILS_IN_SINGLE_GAME_QUESTION = "Would you like to get details in one of these games?"
DETAILS_IN_ANOTHER_GAME_QUESTION = [" Would you like to get details in another game? ", "Would you like to view another game? "]
CHOOSE_GAME_QUESTION = "Which game would you like to see in details? "

IS_USER_TURN = "It is your turn. "
PLACE_A_MOVE_QUESTION = "Would you like to place a move? "
CHOOSE_MOVE_QUESTION = "What move would you like to place? "
                                                  
PLACE_MOVE_SUCCESS = "Move {} placed with success."
PLACE_MOVE_NOT_YOUR_TURN = "Can't place a move, because it is not your turn."

DETAILS_IN_SIGLE_GAME_OVERVIEW = "The game is against {}, who\'s raiting is {}, and you are playing with the {} pieces. "
DETAILS_IN_SIGLE_GAME_LAST_MOVE = "The last move was {}. "
