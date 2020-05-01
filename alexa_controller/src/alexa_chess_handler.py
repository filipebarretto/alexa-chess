# -*- coding: utf-8 -*-

import json
import logging
import boto3
import random
import datetime

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
                                              AbstractRequestHandler, AbstractExceptionHandler,
                                              AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
                                          get_plain_text_content, get_rich_text_content)

from ask_sdk_model.interfaces.display import (
                                              ImageInstance, Image, RenderTemplateDirective, ListTemplate1,
                                              BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response


from custom_modules import utils, data, games, board, account, ratings


# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# STATES
STATE_LAUNCHING = 'state_launching'
STATE_LIST_ALL_ONGOING_GAMES = 'state_list_all_ongoing_games'
STATE_GAME_DETAILS = 'state_game_details'
STATE_PLACE_MOVE = 'state_place_move'
STATE_PLACING_MOVE = 'state_placing_move'
STATE_ANOTHER_GAME_DETAILS = 'state_another_game_details'
STATE_CONFIRM_RESIGNATION = 'state_confirm_resignation'


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        
        attr['state'] = STATE_LAUNCHING
        
        
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        print(user_info)
        
        locale = handler_input.request_envelope.request.locale
        print(locale)
        # en-US
        
        if 'access_token' in user_info:
        
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GETS THE USERNAME FROM LICHESS.ORG
            # TODO: CHECK IF HAS NAME, ELSE USERNAME
            
            username = account.get_username(access_token)
            attr['username'] = username
            
            rsp = (utils.get_random_string_from_list(data.I18N[locale]['WELCOME_MESSAGE'])).format(username)

            response_builder.speak(rsp).ask(utils.get_random_string_from_list(data.I18N[locale]['CHOOSE_ACTION']))
            return handler_input.response_builder.response
        else:
            
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        locale = handler_input.request_envelope.request.locale
        print("Session ended with reason: {}".format(handler_input.request_envelope))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        locale = handler_input.request_envelope.request.locale
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['HELP_MESSAGE'])
        handler_input.response_builder.speak(rsp).ask(rsp)
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        locale = handler_input.request_envelope.request.locale
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['EXIT_SKILL_MESSAGE'])
        handler_input.response_builder.speak(rsp).set_should_end_session(True)
        return handler_input.response_builder.response


# LISTS USER'S ONGOING GAMES
class ListAllOngoingGamesHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("list_all_ongoing_games")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ListAllOngoingGamesHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        locale = handler_input.request_envelope.request.locale
        
        print(user_info)
        print(handler_input.request_envelope.request.locale)
        
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GET ONGOING GAMES LIST
            ongoing_games = games.list_ongoing_games(access_token)
        
            # BUILD ALEXA RESPONSE FOR ONGOING GAMES
            rsp_speak, rsp_card, all_ongoing_games = games.get_ongoing_games_response(ongoing_games, locale)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = utils.get_random_string_from_list(data.I18N[locale]['ONGOING_GAMES_CARD_TITLE']),
                                                      text = rsp_card))
                                                      
            attr['all_ongoing_games'] = all_ongoing_games
            attr['state'] = STATE_LIST_ALL_ONGOING_GAMES
            
            response_builder.speak(rsp_speak).ask(rsp_speak)
            return response_builder.response
        else:
            
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response



class DetailsInAnotherGameHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.YesIntent")(handler_input) and (attr.get('state') == STATE_LIST_ALL_ONGOING_GAMES or attr.get('state') == STATE_ANOTHER_GAME_DETAILS or attr.get('state') == STATE_PLACING_MOVE)
    
    def handle(self, handler_input):
        logger.info("In DetailsInAnotherGameHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale

        attr['state'] = ''
        all_ongoing_games = attr['all_ongoing_games']

        rsp = utils.get_random_string_from_list(data.I18N[locale]['CHOOSE_GAME_QUESTION'])
        response_builder.set_card(ui.StandardCard(
                                          title = utils.get_random_string_from_list(data.I18N[locale]['ONGOING_GAMES_CARD_TITLE']),
                                          text = rsp + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale)))

        response_builder.speak(rsp).ask(rsp)
        return response_builder.response


class CancelGameDetailsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NoIntent")(handler_input) and (attr.get('state') == STATE_LIST_ALL_ONGOING_GAMES or attr.get('state') == STATE_PLACING_MOVE or attr.get('state') == STATE_ANOTHER_GAME_DETAILS)
    
    def handle(self, handler_input):
        logger.info("In CancelGameDetailsHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale

        attr['state'] = ''
        all_ongoing_games = attr['all_ongoing_games']
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['EXIT_SKILL_MESSAGE'])
        
        response_builder.speak(rsp)
        return response_builder.response



# TODO: INCLUDE PROGRESSIVE RESPONSE
class GetGameDetailsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_game_details")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In GetGameDetailsHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        locale = handler_input.request_envelope.request.locale
        
        print('Getting slots...')
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)
        
        # TODO: CONFIRM SLOT RECEIVED
        game_number = slots["game_number"].value
        print("game_number = " + str(game_number))
        
        print('all_ongoing_games')
        all_ongoing_games = attr['all_ongoing_games']
        print(all_ongoing_games)
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            
            username = account.get_username(access_token)
            attr['username'] = username
            print('Getting game details')
            game_details = games.get_game_by_id(access_token, all_ongoing_games[game_number]['gameId'])
            attr['active_game'] = game_details
            
            # BUILD ALEXA RESPONSE
            rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(game_details, username, locale)
            board_image = board.get_board_image(game_details, username)
            
            attr['state'] = STATE_PLACE_MOVE if games.is_player_turn(game_details, username) else STATE_ANOTHER_GAME_DETAILS
            response_builder.speak(rsp_speak).ask(rsp_speak).set_card(ui.StandardCard(
                                                      title = rsp_card_title,
                                                      text = rsp_card_content if games.is_player_turn(game_details, username) else rsp_card_content + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale),
                                                      image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
            
            return response_builder.response
            
        else:
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response



class ChooseMoveHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.YesIntent")(handler_input) and attr.get('state') == STATE_PLACE_MOVE
    
    def handle(self, handler_input):
        logger.info("In ChooseMoveHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        attr['state'] = STATE_PLACING_MOVE
        game_details = attr['active_game']
        username = attr['username']
        
        #username = account.get_username(access_token)
        board_image = board.get_board_image(game_details, username)
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['CHOOSE_MOVE_QUESTION'])
                  
        rsp_title = (utils.get_random_string_from_list(data.I18N[locale]['GAME_DETAILS_CARD_TITLE']).format(games.get_opponent_username(game_details, username), games.get_opponent_rating(game_details, username)))
        
        # TODO: PLACE MOVE HISTORY IN CARD
        response_builder.speak(rsp).ask(rsp).set_card(ui.StandardCard(
                                                  title = rsp_title,
                                                  text = rsp,
                                                  image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                                                  
            
        return response_builder.response


class CancelPlaceMoveHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NoIntent")(handler_input) and attr.get('state') == STATE_PLACE_MOVE
    
    def handle(self, handler_input):
        logger.info("In CancelPlaceMoveHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        all_ongoing_games = attr['all_ongoing_games']
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['OK']) + utils.get_random_string_from_list(data.I18N[locale]['DETAILS_IN_ANOTHER_GAME_QUESTION']) + '\n\n'
        attr['state'] = STATE_ANOTHER_GAME_DETAILS
    
        response_builder.speak(rsp).ask(rsp).set_card(ui.StandardCard(
                                              title = utils.get_random_string_from_list(data.I18N[locale]['ONGOING_GAMES_CARD_TITLE']),
                                              text = rsp + games.get_ongoing_games_list(all_ongoing_games, locale)))
        
        return response_builder.response

# TODO: Place another move when error
class PlaceMoveHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("place_move")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaceMoveHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        locale = handler_input.request_envelope.request.locale
        
        game_details = attr['active_game']
        attr['state'] = STATE_PLACING_MOVE
        all_ongoing_games = attr['all_ongoing_games']
        
        print('Getting slots...')
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)
        
        # GET SPECIAL MOVE SLOT IF EXISTS
        try:
            special_move = slots["special_move"].resolutions.resolutions_per_authority[0].values[0].value.id
            print("Special move: " +  special_move)
        except:
            print("Unable to get special move")
        
        # GET ORIGIN SQUARE SLOT IF EXISTS
        try:
            orig_square = slots["orig_square"].resolutions.resolutions_per_authority[0].values[0].value.id
            print("Origin: " +  orig_square)
        except:
            print("Unable to get origin square")


        # GET DESTINATION SQUARE SLOT IF EXISTS
        try:
            dest_square = slots["dest_square"].resolutions.resolutions_per_authority[0].values[0].value.id
            print("Destination: " +  dest_square)
        except:
            print("Unable to get destination square")
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            username = account.get_username(access_token)
            attr['username'] = username
            
            # CHECKS IF IT IS PLAYER TURN BEFORE PLACING A MOVE
            if games.is_player_turn(game_details, username):
                
                if special_move:
                    print("Move is a special move.")
                    if special_move == 'O-O':
                        response = games.castle_king_size(access_token, game_details, username)
                        print(response)
                    elif special_move == 'O-O-O':
                        response = games.castle_queen_size(access_token, game_details, username)
                        print(response)
                    elif special_move == 'resign':
                        attr['state'] = STATE_CONFIRM_RESIGNATION
                        rsp_speak = utils.get_random_string_from_list(data.I18N[locale]['CONFIRM_RESIGNATION'])
                        response_builder.speak(rsp_speak).ask(rsp_speak)
                        return response_builder.response
                    else:
                        print("Unable to identify special move.")
            
                else:
                    print("Move is a simple move.")
                    move = orig_square + dest_square
                    print('Moving ' + move)
                    response = games.place_move(access_token, game_details['id'], move)
                    print(response)
                
                
                game_details = games.get_game_by_id(access_token, game_details['id'])
                attr['active_game'] = game_details

                rsp_speak, rsp_card = games.get_place_move_response(response, locale, games.get_last_move(game_details))
                rsp_card_title = games.get_game_details_card_title(game_details, username, locale)
                board_image = board.get_board_image(game_details, username)
            
                response_builder.speak(rsp_speak).ask(rsp_speak).set_card(ui.StandardCard(
                                                          title = rsp_card_title,
                                                          text = rsp_card + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale),
                                                          image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                        
                return response_builder.response
        
            else:
        
                rsp = utils.get_random_string_from_list(data.I18N[locale]['PLACE_MOVE_NOT_YOUR_TURN']) + utils.get_random_string_from_list(data.I18N[locale]['DETAILS_IN_ANOTHER_GAME_QUESTION'])
                board_image = board.get_board_image(game_details, username)
                rsp_card_title = games.get_game_details_card_title(game_details, username, locale)
                
                response_builder.speak(rsp).ask(rsp).set_card(ui.StandardCard(
                                                          title = rsp_card_title,
                                                          text = rsp + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale),
                                                          image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                                                          
                return response_builder.response
        
        else:
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response



class ConfirmResignationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.YesIntent")(handler_input) and (attr.get('state') == STATE_CONFIRM_RESIGNATION)
    
    def handle(self, handler_input):
        logger.info("In ConfirmResignationHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        attr['state'] = ''
        username = attr['username']
        game_details = attr['active_game']
        all_ongoing_games = attr['all_ongoing_games']
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token

            # DEBUG
            print('would send a request to resign game')
            #response = games.resign_game(access_token, game_details)
            response = {'status': True, 'message': 'success'}
            print(response)
            
            
            rsp_speak = (utils.get_random_string_from_list(data.I18N[locale]['RESIGNATION_SUCCESS']) if response['status'] else utils.get_random_string_from_list(data.I18N[locale]['RESIGNATION_ERROR'])) + utils.get_random_string_from_list(data.I18N[locale]['CHOOSE_GAME_QUESTION'])
            
            rsp_card = (utils.get_random_string_from_list(data.I18N[locale]['RESIGNATION_SUCCESS']) if response['status'] else utils.get_random_string_from_list(data.I18N[locale]['RESIGNATION_ERROR']))
            
            response_builder.speak(rsp).ask(rsp).set_card(ui.StandardCard(
                                                                          title = utils.get_random_string_from_list(data.I18N[locale]['ONGOING_GAMES_CARD_TITLE']),
                                                                          text = rsp_card + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale)))
                
            return response_builder.response
        
        
        else:
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response
        


class CancelResignationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NoIntent")(handler_input) and (attr.get('state') == STATE_CONFIRM_RESIGNATION)
    
    def handle(self, handler_input):
        logger.info("In CancelResignationHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        attr['state'] = ''
        
        username = attr['username']
        game_details = attr['active_game']
        all_ongoing_games = attr['all_ongoing_games']
        
        # BUILD ALEXA RESPONSE
        rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(game_details, username, locale)
        board_image = board.get_board_image(game_details, username)
        
        attr['state'] = STATE_PLACE_MOVE if games.is_player_turn(game_details, username) else STATE_ANOTHER_GAME_DETAILS
        response_builder.speak(rsp_speak).ask(rsp_speak).set_card(ui.StandardCard(
                                                                                  title = rsp_card_title,
                                                                                  text = rsp_card_content if games.is_player_turn(game_details, username) else rsp_card_content + '\n\n' + games.get_ongoing_games_list(all_ongoing_games, locale),
                                                                                  image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                                                                                      
        return response_builder.response




# RATINGS HANDLERS
class UserRatingHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_user_ratings")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In UserRatingHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        attr['state'] = ''
        
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        
        if 'access_token' in user_info:
            
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GETS THE USERNAME FROM LICHESS.ORG
            resp_speak, resp_card = ratings.get_user_ratings(access_token)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = utils.get_random_string_from_list(data.I18N[locale]['USER_RATINGS_CARD_TITLE']),
                                                      text = resp_card))
            
            response_builder.speak(resp_speak)
            return handler_input.response_builder.response
        else:
            
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response


class UserRatingInSpeedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_user_rating_in_speed")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In UserRatingHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        attr['state'] = ''
        
        print('Getting slots...')
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)
        
        game_speed = slots["game_speed"].resolutions.resolutions_per_authority[0].values[0].value.id
        print("Game Speed: " +  game_speed)
        
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        
        if 'access_token' in user_info:
            
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GETS THE USERNAME FROM LICHESS.ORG
            resp_speak, resp_card = ratings.get_user_ratings_in_speed(access_token, game_speed)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = utils.get_random_string_from_list((data.I18N[locale]['RATING_IN_SPEED_CARD_TITLE']).format(game_speed)),
                                                      text = resp_card))
                
            response_builder.speak(resp_speak)
            return handler_input.response_builder.response
              
        else:
            
            print(data.ERRORS['ERROR_ACCESS_TOKEN'])
            response_builder.speak(utils.get_random_string_from_list(data.I18N[locale]['ERROR_ACCESS_TOKEN_SPEAK']))
            return response_builder.response


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                                                              cached_response_str, Response)
            return cached_response
        else:
            rsp = utils.get_random_string_from_list(data.I18N[locale]['FALLBACK_ANSWER'])
            response_builder.speak(rsp).ask(rsp)
            
            return response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.
        2018-May-01: AMAZON.FallackIntent is only currently available in
        en-US locale. This handler will not be triggered except in that
        locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        locale = handler_input.request_envelope.request.locale
        
        rsp = utils.get_random_string_from_list(data.I18N[locale]['FALLBACK_ANSWER'])
        handler_input.response_builder.speak(rsp).ask(rsp)
                                             
        return handler_input.response_builder.response


# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
        The interceptor is used to cache the handler response that is
        being sent to the user. This can be used to repeat the response
        back to the user, in case a RepeatIntent is being used and the
        skill developer wants to repeat the same information back to
        the user.
        """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response
        locale = handler_input.request_envelope.request.locale


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
        This handler catches all kinds of exceptions and prints
        the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        response_builder = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
    
        rsp_error = utils.get_random_string_from_list(data.I18N[locale]['ERROR_MESSAGE'])
        rsp_help = utils.get_random_string_from_list(data.I18N[locale]['HELP_MESSAGE'])
        handler_input.response_builder.speak(rsp_error).ask(rsp_help)

        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = ""
        
        return handler_input.response_builder.response

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(handler_input.request_envelope))
        locale = handler_input.request_envelope.request.locale


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))
        locale = handler_input.request_envelope.request.locale



# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RepeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())


# Add all request handlers to the skill.
sb.add_request_handler(ListAllOngoingGamesHandler())
sb.add_request_handler(DetailsInAnotherGameHandler())
sb.add_request_handler(CancelGameDetailsHandler())

#sb.add_request_handler(ListMyTurnOngoingGamesHandler())
sb.add_request_handler(GetGameDetailsHandler())
sb.add_request_handler(PlaceMoveHandler())
sb.add_request_handler(CancelPlaceMoveHandler())
sb.add_request_handler(ChooseMoveHandler())
sb.add_request_handler(ConfirmResignationHandler())
sb.add_request_handler(CancelResignationHandler())


sb.add_request_handler(UserRatingHandler())
sb.add_request_handler(UserRatingInSpeedHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()

