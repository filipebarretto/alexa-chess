# -*- coding: utf-8 -*-

import random

URL_LICHESS_API = 'https://lichess.org/'
URL_ACTIVE_GAMES = 'api/account/playing'
URL_SINGLE_GAME = 'game/export/{}'
URL_PLACE_MOVE = 'api/board/game/{}/move/{}'
URL_ACCOUNT = 'api/account'


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
ERROR_ACCESS_TOKEN_SPEAK = ["We had an error retrieving your access token.", "Error retrieving access token"]


MOVE_PIECE_RESPONSE = "Moving piece {} to {}."
ILEGAL_MOVE = "Illegal move. Place a different one."

ONGOING_GAMES_CARD_TITLE = "Ongoing Games"
GAME_DETAILS_CARD_TITLE = "Game against {} ({})"


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
                                                  
PLACE_MOVE_SUCCESS_SPEAK = "Success placing move {move}."
PLACE_MOVE_SUCCESS_CARD = "Move placed: {move}"

PLACE_MOVE_ERROR_SPEAK = "Error placing move {move}."
PLACE_MOVE_ERROR_CARD = "Error placing move."

PLACE_MOVE_NOT_YOUR_TURN = "Can't place a move, because it is not your turn."

DETAILS_IN_SINGLE_GAME_OVERVIEW_SPEAK = "The game is against {opponent}, who\'s raiting is {rating}, and you are playing with the {color} pieces. "
DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_CONTENT = "Opening: {opening}\nMoves: {moves}"
DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE = "Opponent: {opponent} ({rating})"

DETAILS_IN_SINGLE_GAME_LAST_MOVE_SPEAK = "The last move was {move}. "

WITH_CHECK = " with check. "
WITH_CHECKMATE = ", checkmate. "
TAKES_ON = "takes on "
PAWN = "pawn"
CASTLES_KING_SIDE = "castles king side"
CASTLES_QUEEN_SIDE = "castles queen side"
PROMOTING_PIECE = ", promoting to "


PIECE_CODES = {'K': 'king', 'Q': 'queen', 'R': 'rook', 'N': 'knight', 'B': 'bishop'}

