import sys

sys.path.insert(1, '../alexa_controller/')
from custom_modules import data, games, board, ratings


username = "filipebarretto"

# {'game': {}, 'player_color': 'white', , 'player_rating': 1500, 'player_rating_diff': 213 , 'opponent_username': 'TimSeeley', 'opponent_color': 'black', 'opponent_rating': 1562, 'opponent_rating_diff': -85, 'game_status': 'mate', 'opening': 'Italian Game: Two Knights Defense, Fried Liver Attack', 'game_finished': True, 'winner': 'white', 'player_won': True}

gs = [{'game': {"id":"Lgh5mx43","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587650149700,"lastMoveAt":1587650423530,"status":"outoftime","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"provisional":True},"black":{"user":{"name":"MB_Vincent_M_St3","id":"mb_vincent_m_st3"},"rating":1483}},"winner":"white","opening":{"eco":"B00","name":"King's Pawn","ply":1},"moves":"e4","daysPerTurn":2}, 'player_color': 'white', 'player_rating': 1500, 'player_rating_diff': None, 'opponent_username': 'MB_Vincent_M_St3', 'opponent_color': 'black', 'opponent_rating': 1483, 'opponent_rating_diff': None, 'game_status': 'outoftime', 'opening': 'King\'s Pawn', 'game_finished': True, 'winner': 'white',  'player_won': True, 'moves': 'e4', 'lastmove': 'e4'}, {'game': {"id":"Kj2b9bPc","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587650160429,"lastMoveAt":1587652606004,"status":"outoftime","players":{"white":{"user":{"name":"MB_Vincent_M_St3","id":"mb_vincent_m_st3"},"rating":1483,"ratingDiff":-7},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"ratingDiff":61,"provisional":True}},"winner":"black","opening":{"eco":"D00","name":"Queen's Pawn Game","ply":2},"moves":"d4 d5","daysPerTurn":2}, 'player_color': 'black', 'player_rating': 1500, 'player_rating_diff': 61 , 'opponent_username': 'MB_Vincent_M_St3', 'opponent_color': 'white', 'opponent_rating': 1483, 'opponent_rating_diff': -7, 'game_status': 'outoftime', 'opening': 'Queen\'s Pawn Game', 'game_finished': True, 'winner': 'black', 'player_won': True, 'moves': 'd4 d5', 'lastmove': 'd5'}, {'game': {"id":"S27aJ3x6","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587943133162,"lastMoveAt":1588099439180,"status":"mate","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"ratingDiff":213,"provisional":True},"black":{"user":{"name":"TimSeeley","id":"timseeley"},"rating":1562,"ratingDiff":-85,"provisional":True}},"winner":"white","opening":{"eco":"C57","name":"Italian Game: Two Knights Defense, Fried Liver Attack","ply":11},"moves":"e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Ke7 Qf7+ Kd6 Ne4#","daysPerTurn":3}, 'player_color': 'white', 'player_rating': 1500, 'player_rating_diff': 213 , 'opponent_username': 'TimSeeley', 'opponent_color': 'black', 'opponent_rating': 1562, 'opponent_rating_diff': -85, 'game_status': 'mate', 'opening': 'Italian Game: Two Knights Defense, Fried Liver Attack', 'game_finished': True, 'winner': 'white', 'player_won': True, 'moves': 'e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Ke7 Qf7+ Kd6 Ne4#', 'lastmove': 'Ne4#'}, {'game': {"id":"l4e4VxrE","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1587649542870,"lastMoveAt":1588254962937,"status":"started","players":{"white":{"user":{"name":"mrshogi","id":"mrshogi"},"rating":1518,"provisional":True},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1500,"provisional":True}},"opening":{"eco":"D15","name":"Slav Defense: Three Knights Variation","ply":7},"moves":"d4 d5 Nf3 c6 c4 Nf6 Nc3 Bf5 Qb3 Bc8 Bg5 e6 e4 Be7 Bxf6 Bxf6 cxd5 O-O e5 Be7 d6 Bg5 Bd3 Nd7 O-O Bh6 Qc2 g6 Ne4 b5 Qxc6 Nb6 Qxb5 Nd5 g3 Bd7 Qb3 Rb8 Qa3 a5 b3 Nb4 Rfd1 Bc6 Nf6+ Kg7 Ne1 Bg5 Ng4 Nxd3 Rxd3 Be4 Rdd1","daysPerTurn":2}, 'player_color': 'black', 'player_rating': 1500, 'player_rating_diff': None , 'opponent_username': 'mrshogi', 'opponent_color': 'white', 'opponent_rating': 1518, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': 'Slav Defense: Three Knights Variation', 'game_finished': False, 'winner': None, 'player_won': None, 'moves': 'd4 d5 Nf3 c6 c4 Nf6 Nc3 Bf5 Qb3 Bc8 Bg5 e6 e4 Be7 Bxf6 Bxf6 cxd5 O-O e5 Be7 d6 Bg5 Bd3 Nd7 O-O Bh6 Qc2 g6 Ne4 b5 Qxc6 Nb6 Qxb5 Nd5 g3 Bd7 Qb3 Rb8 Qa3 a5 b3 Nb4 Rfd1 Bc6 Nf6+ Kg7 Ne1 Bg5 Ng4 Nxd3 Rxd3 Be4 Rdd1', 'lastmove': 'Rdd1'}, {'game': {"id":"6RkNaMgd","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1588109705400,"lastMoveAt":1588251391641,"status":"started","players":{"white":{"user":{"name":"TimSeeley","id":"timseeley"},"rating":1506,"provisional":True},"black":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1713,"provisional":True}},"opening":{"eco":"B51","name":"Sicilian Defense: Canal-Sokolsky Attack","ply":5},"moves":"e4 c5 Nf3 d6 Bb5+ Nc6 Bxc6+ bxc6 Nc3 e5 d3 Nf6 Bg5 Be7 a3 O-O b4","daysPerTurn":3}, 'player_color': 'black', 'player_rating': 1713, 'player_rating_diff': None , 'opponent_username': 'TimSeeley', 'opponent_color': 'white', 'opponent_rating': 1506, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': 'Sicilian Defense: Canal-Sokolsky Attack', 'game_finished': False, 'winner': None, 'player_won': None, 'moves': 'e4 c5 Nf3 d6 Bb5+ Nc6 Bxc6+ bxc6 Nc3 e5 d3 Nf6 Bg5 Be7 a3 O-O b4', 'lastmove': 'b4'}, {'game': {"id":"zSu4JS09","rated":True,"variant":"standard","speed":"correspondence","perf":"correspondence","createdAt":1588260722402,"lastMoveAt":1588260722402,"status":"started","players":{"white":{"user":{"name":"filipebarretto","id":"filipebarretto"},"rating":1774,"provisional":True},"black":{"user":{"name":"DiscernChess","id":"discernchess"},"rating":1761}},"moves":"","daysPerTurn":1}, 'player_color': 'white', 'player_rating': 1774, 'player_rating_diff': None , 'opponent_username': 'DiscernChess', 'opponent_color': 'black', 'opponent_rating': 1761, 'opponent_rating_diff': None, 'game_status': 'started', 'opening': None, 'game_finished': False, 'winner': None, 'player_won': None, 'moves': '', 'lastmove': ''}]


moves = [{'input': 'Nd5', 'expected_output_move_speak': ' knight to d5', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Qf6', 'expected_output_move_speak': ' queen to f6', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Rxf1', 'expected_output_move_speak': ' rook takes on f1', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Bxf1', 'expected_output_move_speak': ' bishop takes on f1', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Nc3+', 'expected_output_move_speak': ' knight to c3 with check. ', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Nc3#', 'expected_output_move_speak': ' knight to c3, checkmate. ', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'Ndb3', 'expected_output_move_speak': ' knight d to b3', 'expected_output_move_conflict': {'has_conflict': True, 'conflict': 'db'}}, {'input': 'N5d4', 'expected_output_move_speak': ' knight 5 to d4', 'expected_output_move_conflict': {'has_conflict': True, 'conflict': '5d'}}, {'input': 'N5d4#', 'expected_output_move_speak': ' knight 5 to d4, checkmate. ', 'expected_output_move_conflict': {'has_conflict': True, 'conflict': '5d'}}, {'input': 'a8=Q+', 'expected_output_move_speak': 'pawn to a8, promoting to queen with check. ', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}, {'input': 'bxc8=Q+', 'expected_output_move_speak': 'pawn b takes on c8, promoting to queen with check. ', 'expected_output_move_conflict': {'has_conflict': False, 'conflict': None}}]



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

'''
def test_is_player_turn():
    for item in gs:
        assert games.is_player_turn(item['game'], username) == item['opening']
'''

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
    for move in moves:
        assert games.get_move_speak(move['input']) == move['expected_output_move_speak']



# TESTING RESPONSES BUILT

def test_get_game_details_card_title():
    for item in gs:
        assert games.get_game_details_card_title(item['game'], username) == (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE).format(opponent=item['opponent_username'], rating=item['opponent_rating'])


def test_get_game_details_response_speak():
    for item in gs:
        rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username)
        
        base_speak_response = (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_SPEAK).format(opponent=item['opponent_username'], rating=item['opponent_rating'], color=item['player_color']) + ((data.DETAILS_IN_SINGLE_GAME_LAST_MOVE_SPEAK).format(move=games.get_move_speak(games.get_last_move(item['game']))))
        
        if games.is_player_turn(item['game'], username):
            assert rsp_speak == base_speak_response + (data.IS_USER_TURN + data.PLACE_A_MOVE_QUESTION)
        else:
            possible_speak_responses = []
            for s in data.DETAILS_IN_ANOTHER_GAME_QUESTION:
                possible_speak_responses.append(base_speak_response + s + '\n\n')
            assert rsp_speak in possible_speak_responses

def test_get_game_details_response_card_content():
    for item in gs:
        rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username)
        assert rsp_card_content == (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_CONTENT).format(opening=item['opening'], moves=item['moves'])

def test_get_game_details_response_card_title():
    for item in gs:
        rsp_speak, rsp_card_content, rsp_card_title = games.get_game_details_response(item['game'], username)
        assert rsp_card_title == (data.DETAILS_IN_SINGLE_GAME_OVERVIEW_CARD_TITLE).format(opponent=item['opponent_username'], rating=item['opponent_rating'])
