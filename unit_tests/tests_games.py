import sys

sys.path.insert(1, '../alexa_controller/')
from custom_modules import utils, data, games, board, ratings

supported_languages = ["en-US", "pt-BR"]

username = "filipebarretto"

gs_list_raw = [[ {"fullId":"zSu4JS09mMER","gameId":"zSu4JS09","fen":"rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R","color":"white","lastMove":"g8f6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"discernchess","username":"DiscernChess","rating":1761},"isMyTurn":True,"secondsLeft":78220}, {"fullId":"6RkNaMgdj6jc","gameId":"6RkNaMgd","fen":"r1bq1rk1/p3bpp1/2pp1n1p/4p1B1/1P2P3/2NP1N2/2P2PPP/R2QK2R","color":"black","lastMove":"h7h6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"timseeley","username":"TimSeeley","rating":1506},"isMyTurn":False,"secondsLeft":259200}, {"fullId":"l4e4VxrEzMYi","gameId":"l4e4VxrE","fen":"1r1q1r2/6kp/3Pp1p1/p3Ppb1/3Pb1N1/QP4P1/P4P1P/R2RN1K1","color":"black","lastMove":"f7f5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"mrshogi","username":"mrshogi","rating":1518},"isMyTurn":False,"secondsLeft":172800}, {"fullId":"4qPqblkHppfW","gameId":"4qPqblkH","fen":"rn3b1r/p4kp1/1p1ppB1p/2p5/4P3/3Q1N2/PPP2PPP/R3KR2","color":"white","lastMove":"h4f6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"cristianbailen","username":"CristianBailen","rating":1500},"isMyTurn":False,"secondsLeft":172800}, {"fullId":"ganoxiFvEO87","gameId":"ganoxiFv","fen":"r1bqkb1r/1p3ppp/p1nppn2/2p5/P1B1PP2/2N2N2/1PPP2PP/R1BQK2R","color":"black","lastMove":"e7e6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"nominal_reality","username":"Nominal_reality","rating":1734},"isMyTurn":False,"secondsLeft":172800}, {"fullId":"lvNrgaZfAhgW","gameId":"lvNrgaZf","fen":"rnbqkb1r/pppp1ppp/4pn2/8/4P3/2N2N2/PPPP1PPP/R1BQKB1R","color":"white","lastMove":"b1c3","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"lara_12","username":"lara_12","rating":1500},"isMyTurn":False,"secondsLeft":259200}, {"fullId":"87WuzVRpA1jF","gameId":"87WuzVRp","fen":"r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R","color":"white","lastMove":"f3g5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"semenyap123","username":"semenyap123","rating":1500},"isMyTurn":False,"secondsLeft":172800}, {"fullId":"SlB0c3w6WSPd","gameId":"SlB0c3w6","fen":"rnbqkbnr/ppppp1pp/8/5p2/4P3/8/PPPP1PPP/RNBQKBNR","color":"black","lastMove":"f7f5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"mustafa2618","username":"mustafa2618","rating":1500},"isMyTurn":False,"secondsLeft":172800}]]

gs_dict_list = [{1: {"fullId":"zSu4JS09mMER","gameId":"zSu4JS09","fen":"rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R","color":"white","lastMove":"g8f6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"discernchess","username":"DiscernChess","rating":1761},"isMyTurn":True,"secondsLeft":78220},2: {"fullId":"6RkNaMgdj6jc","gameId":"6RkNaMgd","fen":"r1bq1rk1/p3bpp1/2pp1n1p/4p1B1/1P2P3/2NP1N2/2P2PPP/R2QK2R","color":"black","lastMove":"h7h6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"timseeley","username":"TimSeeley","rating":1506},"isMyTurn":False,"secondsLeft":259200},3: {"fullId":"l4e4VxrEzMYi","gameId":"l4e4VxrE","fen":"1r1q1r2/6kp/3Pp1p1/p3Ppb1/3Pb1N1/QP4P1/P4P1P/R2RN1K1","color":"black","lastMove":"f7f5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"mrshogi","username":"mrshogi","rating":1518},"isMyTurn":False,"secondsLeft":172800},4: {"fullId":"4qPqblkHppfW","gameId":"4qPqblkH","fen":"rn3b1r/p4kp1/1p1ppB1p/2p5/4P3/3Q1N2/PPP2PPP/R3KR2","color":"white","lastMove":"h4f6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"cristianbailen","username":"CristianBailen","rating":1500},"isMyTurn":False,"secondsLeft":172800},5: {"fullId":"ganoxiFvEO87","gameId":"ganoxiFv","fen":"r1bqkb1r/1p3ppp/p1nppn2/2p5/P1B1PP2/2N2N2/1PPP2PP/R1BQK2R","color":"black","lastMove":"e7e6","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"nominal_reality","username":"Nominal_reality","rating":1734},"isMyTurn":False,"secondsLeft":172800},6: {"fullId":"lvNrgaZfAhgW","gameId":"lvNrgaZf","fen":"rnbqkb1r/pppp1ppp/4pn2/8/4P3/2N2N2/PPPP1PPP/R1BQKB1R","color":"white","lastMove":"b1c3","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"lara_12","username":"lara_12","rating":1500},"isMyTurn":False,"secondsLeft":259200},7: {"fullId":"87WuzVRpA1jF","gameId":"87WuzVRp","fen":"r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R","color":"white","lastMove":"f3g5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"semenyap123","username":"semenyap123","rating":1500},"isMyTurn":False,"secondsLeft":172800},8: {"fullId":"SlB0c3w6WSPd","gameId":"SlB0c3w6","fen":"rnbqkbnr/ppppp1pp/8/5p2/4P3/8/PPPP1PPP/RNBQKBNR","color":"black","lastMove":"f7f5","variant":{"key":"standard","name":"Standard"},"speed":"correspondence","perf":"correspondence","rated":True,"hasMoved":True,"opponent":{"id":"mustafa2618","username":"mustafa2618","rating":1500},"isMyTurn":False,"secondsLeft":172800}}]

gs = [{'game': {"id":"Lgh5mx43","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587650149700,"lastMoveAt":1587650423530,"status":"outoftime","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"provisional":True},"black":{"user":{"name":"MB_Vincent_M_St3","id":"mb_vincent_m_st3"},"rating":1483}},"winner":"white","opening":{"eco":"B00","name":"King's Pawn","ply":1},"moves":"e4","daysPerTurn":2}, 'player_color': 'white', 'player_rating': 1500, 'player_rating_diff': None, 'opponent_username': 'MB_Vincent_M_St3', 'opponent_color': 'black', 'opponent_rating': 1483, 'opponent_rating_diff': None, 'game_status': 'outoftime', 'opening': 'King\'s Pawn', 'game_finished': True, 'winner': 'white',  'player_won': True, 'moves': 'e4', 'lastmove': 'e4'}, {'game': {"id":"Kj2b9bPc","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587650160429,"lastMoveAt":1587652606004,"status":"outoftime","players":{"white":{"user":{"name":"MB_Vincent_M_St3","id":"mb_vincent_m_st3"},"rating":1483,"ratingDiff":-7},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"ratingDiff":61,"provisional":True}},"winner":"black","opening":{"eco":"D00","name":"Queen's Pawn Game","ply":2},"moves":"d4 d5","daysPerTurn":2}, 'player_color': 'black', 'player_rating': 1500, 'player_rating_diff': 61 , 'opponent_username': 'MB_Vincent_M_St3', 'opponent_color': 'white', 'opponent_rating': 1483, 'opponent_rating_diff': -7, 'game_status': 'outoftime', 'opening': 'Queen\'s Pawn Game', 'game_finished': True, 'winner': 'black', 'player_won': True, 'moves': 'd4 d5', 'lastmove': 'd5'}, {'game': {"id":"S27aJ3x6","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587943133162,"lastMoveAt":1588099439180,"status":"mate","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"ratingDiff":213,"provisional":True},"black":{"user":{"name":"TimSeeley","id":"timseeley"},"rating":1562,"ratingDiff":-85,"provisional":True}},"winner":"white","opening":{"eco":"C57","name":"Italian Game: Two Knights Defense, Fried Liver Attack","ply":11},"moves":"e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Ke7 Qf7+ Kd6 Ne4#","daysPerTurn":3}, 'player_color': 'white', 'player_rating': 1500, 'player_rating_diff': 213 , 'opponent_username': 'TimSeeley', 'opponent_color': 'black', 'opponent_rating': 1562, 'opponent_rating_diff': -85, 'game_status': 'mate', 'opening': 'Italian Game: Two Knights Defense, Fried Liver Attack', 'game_finished': True, 'winner': 'white', 'player_won': True, 'moves': 'e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Ke7 Qf7+ Kd6 Ne4#', 'lastmove': 'Ne4#'}, {'game': {"id":"l4e4VxrE","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587649542870,"lastMoveAt":1588254962937,"status":"started","players":{"white":{"user":{"name":"mrshogi","id":"mrshogi"},"rating":1518,"provisional":True},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"provisional":True}},"opening":{"eco":"D15","name":"Slav Defense: Three Knights Variation","ply":7},"moves":"d4 d5 Nf3 c6 c4 Nf6 Nc3 Bf5 Qb3 Bc8 Bg5 e6 e4 Be7 Bxf6 Bxf6 cxd5 O-O e5 Be7 d6 Bg5 Bd3 Nd7 O-O Bh6 Qc2 g6 Ne4 b5 Qxc6 Nb6 Qxb5 Nd5 g3 Bd7 Qb3 Rb8 Qa3 a5 b3 Nb4 Rfd1 Bc6 Nf6+ Kg7 Ne1 Bg5 Ng4 Nxd3 Rxd3 Be4 Rdd1","daysPerTurn":2}, 'player_color': 'black', 'player_rating': 1500, 'player_rating_diff': None , 'opponent_username': 'mrshogi', 'opponent_color': 'white', 'opponent_rating': 1518, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': 'Slav Defense: Three Knights Variation', 'game_finished': False, 'winner': None, 'player_won': None, 'moves': 'd4 d5 Nf3 c6 c4 Nf6 Nc3 Bf5 Qb3 Bc8 Bg5 e6 e4 Be7 Bxf6 Bxf6 cxd5 O-O e5 Be7 d6 Bg5 Bd3 Nd7 O-O Bh6 Qc2 g6 Ne4 b5 Qxc6 Nb6 Qxb5 Nd5 g3 Bd7 Qb3 Rb8 Qa3 a5 b3 Nb4 Rfd1 Bc6 Nf6+ Kg7 Ne1 Bg5 Ng4 Nxd3 Rxd3 Be4 Rdd1', 'lastmove': 'Rdd1'}, {'game': {"id":"6RkNaMgd","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1588109705400,"lastMoveAt":1588251391641,"status":"started","players":{"white":{"user":{"name":"TimSeeley","id":"timseeley"},"rating":1506,"provisional":True},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1713,"provisional":True}},"opening":{"eco":"B51","name":"Sicilian Defense: Canal-Sokolsky Attack","ply":5},"moves":"e4 c5 Nf3 d6 Bb5+ Nc6 Bxc6+ bxc6 Nc3 e5 d3 Nf6 Bg5 Be7 a3 O-O b4","daysPerTurn":3}, 'player_color': 'black', 'player_rating': 1713, 'player_rating_diff': None , 'opponent_username': 'TimSeeley', 'opponent_color': 'white', 'opponent_rating': 1506, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': 'Sicilian Defense: Canal-Sokolsky Attack', 'game_finished': False, 'winner': None, 'player_won': None, 'moves': 'e4 c5 Nf3 d6 Bb5+ Nc6 Bxc6+ bxc6 Nc3 e5 d3 Nf6 Bg5 Be7 a3 O-O b4', 'lastmove': 'b4'}, {'game': {"id":"zSu4JS09","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1588260722402,"lastMoveAt":1588260722402,"status":"started","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1774,"provisional":True},"black":{"user":{"name":"DiscernChess","id":"discernchess"},"rating":1761}},"moves":"","daysPerTurn":1}, 'player_color': 'white', 'player_rating': 1774, 'player_rating_diff': None , 'opponent_username': 'DiscernChess', 'opponent_color': 'black', 'opponent_rating': 1761, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': None, 'game_finished': False, 'winner': None, 'player_won': None, 'moves': '', 'lastmove': ''}]


moves = [{'input': 'Nd5', 'expected_output_move_speak': {'en-US': ' knight to d5', 'pt-BR': ' cavalo para d5'}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Qf6', 'expected_output_move_speak': {'en-US': ' queen to f6', 'pt-BR': ' rainha para f6'}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Rxf1', 'expected_output_move_speak': {'en-US': ' rook takes on f1', 'pt-BR': ' torre toma em f1'}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Bxf1', 'expected_output_move_speak': {'en-US': ' bishop takes on f1', 'pt-BR': ' bispo toma em f1'}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Nc3+', 'expected_output_move_speak': {'en-US': ' knight to c3 with check. ', 'pt-BR': ' cavalo para c3 com cheque. '}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Nc3#', 'expected_output_move_speak': {'en-US': ' knight to c3, checkmate. ', 'pt-BR': ' cavalo para c3, cheque-mate. '}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Ndb3', 'expected_output_move_speak': {'en-US': ' knight d to b3', 'pt-BR': ' cavalo d para b3'}, 'expected_output_move_conflict': {'has_conflict': True, 'conflict': 'db'}}, {'input': 'N5d4', 'expected_output_move_speak': {'en-US': ' knight 5 to d4', 'pt-BR': ' cavalo 5 para d4'}, 'expected_output_move_conflict': {'has_conflict': True, 'conflict': '5d'}}, {'input': 'N5d4#', 'expected_output_move_speak': {'en-US': ' knight 5 to d4, checkmate. ', 'pt-BR': ' cavalo 5 para d4, cheque-mate. '}, 'expected_output_move_conflict': {'has_conflict': True, 'conflict': '5d'}}, {'input': 'a8=Q+', 'expected_output_move_speak': {'en-US': 'pawn to a8, promoting to queen with check. ', 'pt-BR': 'peão para a8, promovendo para rainha com cheque. '}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'bxc8=Q+', 'expected_output_move_speak': {'en-US': 'pawn b takes on c8, promoting to queen with check. ', 'pt-BR': 'peão b toma em c8, promovendo para rainha com cheque. '}, 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}]



def test_get_opponent_username():
    for item in gs:
        assert games.get_opponent_username(item['game'], username) == item['opponent_username']

def test_get_opponent_color():
    for item in gs:
        assert games.get_opponent_color(item['game'], username) == item['opponent_color']

def test_get_opponent_rating():
    for item in gs:
        assert games.get_opponent_rating(item['game'], username) == item['opponent_rating']

def test_get_player_color():
    for item in gs:
        assert games.get_player_color(item['game'], username) == item['player_color']

def test_get_player_rating():
    for item in gs:
        assert games.get_player_rating(item['game'], username) == item['player_rating']


def test_get_game_opening():
    for item in gs:
        assert games.get_game_opening(item['game']) == item['opening']

def test_get_game_finished():
    for item in gs:
        assert games.get_game_finished(item['game']) == item['game_finished']

def test_get_game_winner():
    for item in gs:
        assert games.get_game_winner(item['game']) == item['winner']

def test_get_player_won():
    for item in gs:
        assert games.get_player_won(item['game'], username) == item['player_won']

def test_get_last_move():
    for item in gs:
        assert games.get_last_move(item['game']) == item['lastmove']

def test_checks_source_square_conflict():
    for move in moves:
        assert games.checks_source_square_conflict(move['input']) == move['expected_output_move_conflict']

def test_get_move_speak():
    for language in supported_languages:
        for move in moves:
            assert games.get_move_speak(move['input'], language) == move['expected_output_move_speak'][language]


def get_ongoing_games_list(ongoing_games_dict, locale):
    response = ''
    for key, game in ongoing_games_dict.items():
        response += (utils.get_random_string_from_list(data.I18N[locale]['LIST_GAMES_ITEM'])).format(game_number=key, opponent=game['opponent']['username'], color=data.COLORS[locale][game['color']]) + (utils.get_random_string_from_list(data.I18N[locale]['LIST_GAMES_ITEM_PLAYER_TURN']) if game['isMyTurn'] else '') + '\n'
    return response

# GAMES LIST
def test_get_ongoing_games_list():
    MAX_NUM_GAME_LIST = 3
    for gs_dict in gs_dict_list:
        for language in supported_languages:
            ongoing_games_response = games.get_ongoing_games_list(gs_dict, language)
            possible_responses = []
            
            for j in range(len(data.I18N[language]['LIST_GAMES_ITEM'])):
                for k in range(len(data.I18N[language]['LIST_GAMES_ITEM_PLAYER_TURN'])):
                    possible_response = ''
                    for key, game in gs_dict.items():
                        possible_response += (data.I18N[language]['LIST_GAMES_ITEM'][j]).format(game_number=key, opponent=game['opponent']['username'], color=data.COLORS[language][game['color']]) + (data.I18N[language]['LIST_GAMES_ITEM_PLAYER_TURN'][k] if game['isMyTurn'] else '') + '\n'
        
                    possible_responses.append(possible_response)
            
            assert ongoing_games_response in possible_responses
            


def test_get_ongoing_games_response():
    MAX_NUM_GAME_LIST = 3
    for gs_list in gs_list_raw:
        for language in supported_languages:
            speak_response, card_response, ongoing_games_dict = games.get_ongoing_games_response(gs_list, language)
            
            possible_responses = []
            possible_response = ''
            for j in range(len(data.I18N[language]['LIST_GAMES_NUMBER_OF_GAMES'])):
                for k in range(len(data.I18N[language]['LIST_GAMES_SOME_GAMES'])):
                    for l in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_QUESTION'])):
                        possible_response += (data.I18N[language]['LIST_GAMES_NUMBER_OF_GAMES'][j]).format(active_games=len(gs_list), active_games_player_turn=1) + (data.I18N[language]['LIST_GAMES_SOME_GAMES'][k]).format(some_games=games.get_ongoing_games_opponents_response(ongoing_games_dict, language)) + (data.I18N[language]['DETAILS_IN_SINGLE_GAME_QUESTION'][l])
            possible_responses.append(possible_response)
        

            assert speak_response in possible_responses



# TESTING RESPONSES BUILT

def test_get_game_details_card_title():
    possible_responses = []
    for item in gs:
        for language in supported_languages:
            for i in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE'])):
                possible_responses.append((data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE'][i]).format(opponent=item['opponent_username'], rating=item['opponent_rating']))

    assert games.get_game_details_card_title(item['game'], username, language) in possible_responses



def test_get_game_details_response_speak():
    for language in supported_languages:
        for item in gs:
            possible_responses = []
            rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username, language)
            
            for i in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_SPEAK'])):
                for j in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_LAST_MOVE_SPEAK'])):
                    base_speak_response = (data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_SPEAK'][i]).format(opponent=item['opponent_username'], rating=item['opponent_rating'], color=data.COLORS[language][item['player_color']]) + ((data.I18N[language]['DETAILS_IN_SINGLE_GAME_LAST_MOVE_SPEAK'][j]).format(move=games.get_move_speak(games.get_last_move(item['game']), language)))
    
                    if games.is_player_turn(item['game'], username):
                        for k in range(len(data.I18N[language]['IS_USER_TURN'])):
                            for l in range(len(data.I18N[language]['PLACE_A_MOVE_QUESTION'])):
                                possible_responses.append(base_speak_response + (data.I18N[language]['IS_USER_TURN'][k] + data.I18N[language]['PLACE_A_MOVE_QUESTION'][l]))
                    else:
                        for m in range(len(data.I18N[language]['DETAILS_IN_ANOTHER_GAME_QUESTION'])):
                            possible_responses.append(base_speak_response + data.I18N[language]['DETAILS_IN_ANOTHER_GAME_QUESTION'][m] + '\n\n')

            assert rsp_speak in possible_responses


def test_get_game_details_response_card_content():
    for language in supported_languages:
        for item in gs:
            possible_responses = []
            rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username, language)
            
            for i in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_CONTENT'])):
                possible_responses.append((data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_CONTENT'][i]).format(opening=item['opening'], moves=item['moves']))

            assert rsp_card_content in possible_responses


def test_get_game_details_response_card_title():
    for language in supported_languages:
        for item in gs:
            possible_responses = []
            rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username, language)
            
            for i in range(len(data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE'])):
                possible_responses.append((data.I18N[language]['DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE'][i]).format(opponent=item['opponent_username'], rating=item['opponent_rating']))
            
            assert rsp_card_title in possible_responses
            
