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


from custom_modules import data, games, board, account, ratings


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
        print(handler_input.request_envelope.request.locale)
        # en-US
        
        if 'access_token' in user_info:
        
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GETS THE USERNAME FROM LICHESS.ORG
            firstname = account.get_username(access_token)
            rsp = (data.WELCOME_MESSAGE).format(firstname)
            
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
        
            response_builder.speak(rsp).ask(rand.choice(data.CHOOSE_ACTION))
            return handler_input.response_builder.response
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
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
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session
        
        handler_input.response_builder.speak(data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
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
        handler_input.response_builder.speak(
                                             data.EXIT_SKILL_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response



# LISTS 3 MOST RECENT USER ONGOING GAMES
'''
class ListMyTurnOngoingGamesHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("list_my_turn_ongoing_games")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ListMyTurnOngoingGamesHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        
        print(user_info)
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            ongoing_games = games.list_ongoing_games(access_token)
            
            attr['ongoing_games'] = ongoing_games
            
            # BUILD ALEXA RESPONSE
            rsp = games.build_ongoing_games_response(ongoing_games)
            response_builder.speak(rsp)
            return response_builder.response
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response
'''

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
        
        print(user_info)
        
        print(handler_input.request_envelope.request.locale)
        
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GET ONGOING GAMES LIST
            ongoing_games = games.list_ongoing_games(access_token)
        
            # BUILD ALEXA RESPONSE FOR ONGOING GAMES
            rsp_speak, rsp_card, all_ongoing_games = games.get_ongoing_games_response(ongoing_games)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = data.ONGOING_GAMES_CARD_TITLE,
                                                      text = rsp_card))
                                                      
            attr['all_ongoing_games'] = all_ongoing_games
            attr['state'] = STATE_LIST_ALL_ONGOING_GAMES
            
            response_builder.speak(rsp_speak).ask(rsp_speak)
            return response_builder.response
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response



class DetailsInAnotherGameHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.YesIntent")(handler_input) and (attr.get('state') == STATE_LIST_ALL_ONGOING_GAMES or attr.get('state') == STATE_ANOTHER_GAME_DETAILS or attr.get('state') == STATE_PLACING_MOVE)
    
    def handle(self, handler_input):
        logger.info("In DetailsInAnotherGameHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder

        attr['state'] = ''
        all_ongoing_games = attr['all_ongoing_games']

        rsp = data.CHOOSE_GAME_QUESTION
        response_builder.set_card(ui.StandardCard(
                                          title = data.ONGOING_GAMES_CARD_TITLE,
                                          text = rsp + '\n\n' + games.get_ongoing_games_list(all_ongoing_games)))

        response_builder.speak(rsp).ask(rsp)
        return response_builder.response


class CancelGameDetailsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NoIntent")(handler_input) and (attr.get('state') == STATE_LIST_ALL_ONGOING_GAMES or attr.get('state') == STATE_PLACING_MOVE)
    
    def handle(self, handler_input):
        logger.info("In CancelGameDetailsHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder

        attr['state'] = ''
        all_ongoing_games = attr['all_ongoing_games']
        
        rsp = data.EXIT_SKILL_MESSAGE
        
        response_builder.speak(rsp)
        return response_builder.response



class GetGameDetailsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_game_details")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In GetGameDetailsHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        
        print('Getting slots...')
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)
        
        game_number = slots["game_number"].value
        print("game_number = " + str(game_number))
        
        print('all_ongoing_games')
        all_ongoing_games = attr['all_ongoing_games']
        print(all_ongoing_games)
        
        print('game_details')
        game_details = all_ongoing_games[game_number]
        print(game_details)
        attr['active_game'] = game_details

        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            
            # BUILD ALEXA RESPONSE
            rsp, my_turn = games.get_game_details_response(game_details)
            
            board_image = board.get_board_image(game_details['gameId'], game_details['fen'], game_details['color'], game_details['lastMove'])
            
            if my_turn:
                rsp += data.IS_USER_TURN + data.PLACE_A_MOVE_QUESTION
                attr['state'] = STATE_PLACE_MOVE
                response_builder.speak(rsp).ask(rsp)
            else:
                ts = datetime.datetime.now().timestamp()
                rand = random.Random(int(ts))
            
                rsp += rand.choice(data.DETAILS_IN_ANOTHER_GAME_QUESTION) + '\n\n'
                attr['state'] = STATE_ANOTHER_GAME_DETAILS
                response_builder.speak(rsp).ask(rsp)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = (data.GAME_DETAILS_CARD_TITLE).format(game_details['opponent']['username']),
                                                      text = rsp if my_turn else rsp + games.get_ongoing_games_list(all_ongoing_games),
                                                      image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
            
            return response_builder.response
            
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response



class ChooseMoveHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.YesIntent")(handler_input) and attr.get('state') == STATE_PLACE_MOVE
    
    def handle(self, handler_input):
        logger.info("In ChooseMoveHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        
        attr['state'] = STATE_PLACING_MOVE
        game_details = attr['active_game']
        board_image = board.get_board_image(game_details['gameId'], game_details['fen'], game_details['color'], game_details['lastMove'])
        
        rsp = data.CHOOSE_MOVE_QUESTION
        
        # TODO: PLACE MOVE HISTORY IN CARD
        response_builder.set_card(ui.StandardCard(
                                                  title = (data.GAME_DETAILS_CARD_TITLE).format(game_details['opponent']['username']),
                                                  text = rsp,
                                                  image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                                                  
            
        response_builder.speak(rsp).ask(rsp)
        return response_builder.response


class CancelPlaceMoveHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NoIntent")(handler_input) and attr.get('state') == STATE_PLACE_MOVE
    
    def handle(self, handler_input):
        logger.info("In CancelPlaceMoveHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        
        all_ongoing_games = attr['all_ongoing_games']
        
        ts = datetime.datetime.now().timestamp()
        rand = random.Random(int(ts))
        
        rsp = data.OK + rand.choice(data.DETAILS_IN_ANOTHER_GAME_QUESTION) + '\n\n'
        attr['state'] = STATE_ANOTHER_GAME_DETAILS
    
        response_builder.set_card(ui.StandardCard(
                                              title = data.ONGOING_GAMES_CARD_TITLE,
                                              text = rsp + games.get_ongoing_games_list(all_ongoing_games)))
        
        response_builder.speak(rsp).ask(rsp)
        return response_builder.response


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
        
        active_game = attr['active_game']
        attr['state'] = STATE_PLACING_MOVE
        
        print('Getting slots...')
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)
        
        orig_square = slots["orig_square"].resolutions.resolutions_per_authority[0].values[0].value.id
        print("Origin: " +  orig_square)
        
        dest_square = slots["dest_square"].resolutions.resolutions_per_authority[0].values[0].value.id
        print("Destination: " +  dest_square)
        
        move = orig_square + dest_square
        print('Moving ' + move)
        
        if 'access_token' in user_info:
            access_token = handler_input.request_envelope.session.user.access_token
            
            # CHECKS IF IT IS PLAYER TURN BEFORE PLACING A MOVE
            if active_game['isMyTurn']:
                response = games.place_move(access_token, active_game['gameId'], move)
                print(response)
                rsp = response['message']
                
                game, ongoing_games = games.get_game_by_id(access_token, active_game['gameId'])
                
                rsp_speak, rsp_card, all_ongoing_games = games.get_ongoing_games_response(ongoing_games)
                attr['all_ongoing_games'] = all_ongoing_games
                
                response_builder.speak(rsp).ask(rsp)
                
                board_image = board.get_board_image(game['gameId'], game['fen'], game['color'], game['lastMove'])
            
                response_builder.set_card(ui.StandardCard(
                                                          title = (data.GAME_DETAILS_CARD_TITLE).format(game['opponent']['username']),
                                                          text = rsp + '\n' + rsp_card,
                                                          image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                    
                return response_builder.response
    
            else:
                
                ts = datetime.datetime.now().timestamp()
                rand = random.Random(int(ts))
        
                rsp = data.PLACE_MOVE_NOT_YOUR_TURN + rand.choice(data.DETAILS_IN_ANOTHER_GAME_QUESTION)
                
                rsp_speak, rsp_card, all_ongoing_games = games.get_ongoing_games_response(ongoing_games)
                attr['all_ongoing_games'] = all_ongoing_games
                
                response_builder.speak(rsp).ask(rsp)
                
                board_image = board.get_board_image(game['gameId'], game['fen'], game['color'], game['lastMove'])
                
                response_builder.set_card(ui.StandardCard(
                                                          title = (data.GAME_DETAILS_CARD_TITLE).format(game['opponent']['username']),
                                                          text = rsp + '\n\n' + games.get_ongoing_games_list(all_ongoing_games),
                                                          image = ui.Image(small_image_url = board_image, large_image_url = board_image)))
                                                          
                return response_builder.response
        
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response



# RATINGS HANDLERS
class UserRatingHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_user_ratings")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In UserRatingHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        
        attr['state'] = ''
        
        user_info = handler_input.request_envelope.session.user
        user_info = user_info.to_dict()
        
        if 'access_token' in user_info:
            
            access_token = handler_input.request_envelope.session.user.access_token
            
            # GETS THE USERNAME FROM LICHESS.ORG
            resp_speak, resp_card = ratings.get_user_ratings(access_token)
            
            response_builder.set_card(ui.StandardCard(
                                                      title = data.USER_RATINGS_CARD_TITLE,
                                                      text = resp_card))
            
            response_builder.speak(resp_speak)
            return handler_input.response_builder.response
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
            return response_builder.response


class UserRatingInSpeedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("get_user_rating_in_speed")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In UserRatingHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        
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
                                                      title = (data.RATING_IN_SPEED_CARD_TITLE).format(game_speed),
                                                      text = resp_card))
                
            response_builder.speak(resp_speak)
            return handler_input.response_builder.response
              
        else:
            ts = datetime.datetime.now().timestamp()
            rand = random.Random(int(ts))
            
            print(rand.choice(data.ERROR_ACCESS_TOKEN))
            response_builder.speak(rand.choice(data.ERROR_ACCESS_TOKEN_SPEAK))
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
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                                                              cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.FALLBACK_ANSWER)
            
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
        handler_input.response_builder.speak(
                                             data.FALLBACK_ANSWER).ask(data.FALLBACK_ANSWER)
                                             
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
        
        handler_input.response_builder.speak(data.ERROR_MESSAGE).ask(data.HELP_MESSAGE)
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = ""
        
        return handler_input.response_builder.response

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
                                                  handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))



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
