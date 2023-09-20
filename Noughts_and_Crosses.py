import re
from types import MethodType

num_draws = 0
game_not_endded = True

#players
class player:
    num_wins = 0
    is_AI = False
    difficulty = 0
    def __init__(self, pname, counter, turn_no=0):
        self.name = 'Player ' + pname
        self.counter = counter
        self.turn_no = turn_no

players = [player('1', '0'), player('2', 'X', turn_no=1)]
player_no = 0
curr_player = players[player_no]

def using_singleplayer():
    global players

    game_is_singleplayer = False

    for i in range(len(players)):
        if players[i].is_AI:
            game_is_singleplayer = True
            break

    return game_is_singleplayer

def setup_game_settings():
    global players

    game_mode_is_invalid = True

    while game_mode_is_invalid:
        game_mode = raw_input('\nPlay multiplayer or singleplayer?\n')
        game_mode = re.sub(r'\s+', '', game_mode.lower())

        if game_mode == 'singleplayer':
            AI_turn_no_is_invalid = True

            while AI_turn_no_is_invalid:
                AI_turn_no = raw_input('\nDo you want the AI to have first turn?\nChoose from yes or no.\n')
                AI_turn_no = re.sub(r'\s+', '', AI_turn_no.lower())

                if AI_turn_no == 'yes':
                    players[0].name = 'AI'
                    players[1].name = 'Player 1'
                    AI_turn_no = 0
                    AI_turn_no_is_invalid = False

                elif AI_turn_no == 'no':
                    players[1].name = 'AI'
                    players[0].name = 'Player 1'
                    AI_turn_no = 1
                    AI_turn_no_is_invalid = False

                else:
                    print('Invaild option. Try again.')

            AI_difficulty_is_invalid = True

            while AI_difficulty_is_invalid:
                AI_difficulty = raw_input('\nHow difficult do you want the AI to be? The lower the number, the easier.\nYou can choose from:\n1\n2\n3\n')
                AI_difficulty = int(re.sub(r'\s+', '', AI_difficulty))

                if AI_difficulty == 1 or AI_difficulty == 2 or AI_difficulty == 3:
                    players[AI_turn_no].difficulty = AI_difficulty
                    AI_difficulty_is_invalid = False

                else:
                    print('Invaild option. Try again.') 

            players[AI_turn_no].is_AI = True
            players[AI_turn_no].turn_no = AI_turn_no

            game_mode_is_invalid = False

        elif game_mode == 'multiplayer':
            game_mode_is_invalid = False

        else:
            print('Invalid option. Try again.')
    
    for i in range(len(players)):
        if not players[i].is_AI:
            new_player_name = raw_input('\n' + players[i].name + ', enter your prefered name.\n')

            if new_player_name <> '':
                #to do: reuse players if new_player_name is already being used
                players[i].name = new_player_name
            print(players[i].name + ', your counter is ' + players[i].counter + '.')

def get_human_player():
    if using_singleplayer():
        human_player = ''

        if players[0].is_AI:
            human_player = players[1]
        else:
            human_player = players[0]

        return human_player

def get_AI_player():
    if using_singleplayer():
        AI_player = ''

        if players[0].is_AI:
            AI_player = players[0]
        else:
            AI_player = players[1]

        return AI_player

def switch_player():
    global players
    global player_no
    global curr_player

    #if player number higher than num of players
    if player_no == len(players)-1:
        #reset player number
        player_no = 0
    else:
        #increase player number
        player_no =+ 1

    curr_player = players[player_no]

#board

class board:
    positions = []
    visual_txt = ''

def print_board(self):
    self.visual_txt = '\nBoard:\n'

    for i in range(len(self.positions)):
        col_middle = (i == 1 or i == 4 or i == 7)

        if col_middle:
            self.visual_txt += '|'

        if board.positions[i].owner == None:
            self.visual_txt += '-'
        else:
            self.visual_txt += board.positions[i].owner.counter

        if col_middle:
            self.visual_txt += '|'
        if i == 2 or i == 5:
            self.visual_txt += '\n'

    print(self.visual_txt)

board._print = MethodType(print_board, board, board)

class position:
    owner = None
    def __init__(self, id, pos_name):
        self.id = id;
        self.name = pos_name

#create the positions on the board
for i in range(9):
    vert_dir = ''
    horz_dir = ''

    if i < 3:
        vert_dir = 'top '
    elif i < 6:
        vert_dir = 'middle '
    else:
        vert_dir = 'bottom '

    if i == 0 or i == 3 or i == 6:
         horz_dir = 'left'
    if i == 1 or i == 4 or i == 7:
        horz_dir = 'middle'
    if i == 2 or i == 5 or i == 8:
        horz_dir = 'right'

    pos_name = vert_dir + horz_dir

    if i == 4:
        pos_name = 'centre'

    board.positions.append(position(i, pos_name))

def get_available_positions(get_pos_names=False):
    #get a list of which places aren't owned by a player
    available_positions = None

    if get_pos_names:
        available_positions = ''
    else:
        available_positions = []

    for i in range(len(board.positions)):
        if board.positions[i].owner == None:
            if get_pos_names:
                available_positions += board.positions[i].name + '\n'

            else:
                available_positions.append(board.positions[i])

    return available_positions

def get_position_owner(place, modify_owner=False):
    global curr_player
    global board
    for i in range(len(board.positions)):
        if board.positions[i].name == place:
            if modify_owner:
                board.positions[i].owner = curr_player
            break

    return board.positions[i].owner

def position_owner_is_none(place):
    if get_position_owner(place) == None:
        return True

    else:
        return False

def get_positions_by_owner(_player, get_ids=False, get_names=False):
    global board

    owned_positions = []

    for i in range(len(board.positions)):
        if board.positions[i].owner == _player:
            if get_ids:
                owned_positions.append(board.positions[i].id)
            elif get_names:
                owned_positions.append(board.positions[i].name)
            else:
                owned_positions.append(board.positions[i])

    return owned_positions

def AI_decide_place():
    global curr_player
    global board

    chosen_place = ''
    opponent = get_human_player()
    self = get_AI_player()
    num_opponent_corners = 0
    num_own_corners = 0

    if curr_player.difficulty == 1:
        #go for any place that doesn't have an owner
        for i in range(len(board.positions)):
            if board.positions[i].owner == None:
                chosen_place = board.positions[i].name
                break

    if curr_player.difficulty == 2:
        #go for corners if possible
        if position_owner_is_none('top left'):
            chosen_place = 'top left'
        elif position_owner_is_none('top right'):
            chosen_place = 'top right'
        elif position_owner_is_none('bottom left'):
            chosen_place = 'bottom left'
        elif position_owner_is_none('bottom right'):
            chosen_place = 'bottom right'

        #then try to get the 'middle' place
        elif position_owner_is_none('centre'):
            chosen_place = 'centre'
        elif position_owner_is_none('middle left'):
            chosen_place = 'middle left'
        elif position_owner_is_none('middle right'):
            chosen_place = 'middle right'
        elif position_owner_is_none('bottom middle'):
            chosen_place = 'bottom middle'
        else:
            chosen_place = 'top middle'
 
    if curr_player.difficulty == 3:
        #get the number of corners each player has
        human_positions = get_positions_by_owner(opponent, get_names=True)
        for i in range(len(human_positions)):
            if human_positions[i] == 'top left' or human_positions[i] == 'top right' or human_positions[i] == 'bottom left' or human_positions[i] == 'bottom right':
                num_opponent_corners += 1
    
        AI_positions = get_positions_by_owner(self, get_names=True)
        for i in range(len(AI_positions)):
            if AI_positions[i] == 'top left' or AI_positions[i] == 'top right' or AI_positions[i] == 'bottom left' or AI_positions[i] == 'bottom right':
                num_own_corners += 1

        #go for 1 more corner than what the oppenent has
        #deciding to go for a corner or middle
        if curr_player.turn_no == 0 and (num_opponent_corners + 2) > num_own_corners and (num_own_corners + num_opponent_corners) < 4:
            #go for a corner if there's a corner avilable

            for i in range(len(board.positions)):
                if board.positions[i].owner == None:
                    if board.positions[i].name == 'top left' or board.positions[i].name == 'top right' or board.positions[i].name == 'bottom left' or board.positions[i].name == 'bottom right':
                        chosen_place = board.positions[i].name
                        break

        elif curr_player.turn_no == 1 and (num_opponent_corners + 1) > num_own_corners and (num_own_corners + num_opponent_corners) < 4:
            #go for a corner if there's a corner avilable
            #AI needs to know where opponent will go 1 before the opponent plays if AI hasn't got first turn
            for i in range(len(board.positions)):
                if board.positions[i].owner == None:
                    if board.positions[i].name == 'top left' or board.positions[i].name == 'top right' or board.positions[i].name == 'bottom left' or board.positions[i].name == 'bottom right':
                        chosen_place = board.positions[i].name
                        break

        else:
            #go for a 'middle' place - logically decides which middle place to go for
            for i in range(len(board.positions)):
                if board.positions[i].owner == None:
                    if 'centre' in str(board.positions[i].name):
                            chosen_place = board.positions[i].name
                            break
                    if len(re.findall('top', str(AI_positions))) > 1:
                        if 'top' in str(board.positions[i].name):
                            chosen_place = board.positions[i].name
                            break
                    if len(re.findall('bottom', str(AI_positions))) > 1:
                        if 'bottom' in str(board.positions[i].name):
                            chosen_place = board.positions[i].name
                            break
                    if len(re.findall('left', str(AI_positions))) > 1:
                        if 'left' in str(board.positions[i].name):
                            chosen_place = board.positions[i].name
                            break
                    if len(re.findall('right', str(AI_positions))) > 1:
                        if 'right' in str(board.positions[i].name):
                            chosen_place = board.positions[i].name
                            break

            if chosen_place == '':
                #decide where human will go next and go for that position
                human_positions_ids = get_positions_by_owner(opponent, get_ids=True)
                row_top = [0, 1, 2]###
                row_middle = [3, 4, 5]###
                row_bottom = [6, 7, 8]###
                col_left = [0, 3, 6]###
                col_middle = [1, 4, 7]###
                col_right = [2, 5, 8]###
                di_ltr = [0, 4, 8]###
                di_rtl = [2, 4, 6]###

                if position_owner_is_none('top left'):
                    if 1 in human_positions_ids and 2 in human_positions_ids or 3 in human_positions_ids and 6 in human_positions_ids or 4 in human_positions_ids and 8 in human_positions_ids:
                        chosen_place = 'top left'

                if position_owner_is_none('top middle'):
                    if 0 in human_positions_ids and 2 in human_positions_ids or 4 in human_positions_ids and 7 in human_positions_ids:
                        chosen_place = 'top middle'

                if position_owner_is_none('top right'):
                    if 0 in human_positions_ids and 1 in human_positions_ids or 5 in human_positions_ids and 8 in human_positions_ids or 4 in human_positions_ids and 6 in human_positions_ids:
                        chosen_place = 'top right'

                if position_owner_is_none('middle left'):
                    if 4 in human_positions_ids and 5 in human_positions_ids or 0 in human_positions_ids and 6 in human_positions_ids:
                        chosen_place = 'middle left'

                if position_owner_is_none('centre'):
                    if 3 in human_positions_ids and 5 in human_positions_ids or 1 in human_positions_ids and 7 in human_positions_ids or 0 in human_positions_ids and 8 in human_positions_ids or 2 in human_positions_ids and 6 in human_positions_ids:
                        chosen_place = 'centre'

                if position_owner_is_none('middle right'):
                    if 3 in human_positions_ids and 4 in human_positions_ids or 2 in human_positions_ids and 8 in human_positions_ids:
                        chosen_place = 'middle right'

                if position_owner_is_none('bottom left'):
                    if 7 in human_positions_ids and 8 in human_positions_ids or 0 in human_positions_ids and 3 in human_positions_ids or 2 in human_positions_ids and 4 in human_positions_ids:
                        chosen_place = 'bottom left'

                if position_owner_is_none('bottom middle'):
                    if 6 in human_positions_ids and 8 in human_positions_ids or 1 in human_positions_ids and 4 in human_positions_ids:
                        chosen_place = 'bottom middle'

                if position_owner_is_none('bottom right'):
                    if 6 in human_positions_ids and 7 in human_positions_ids or 2 in human_positions_ids and 5 in human_positions_ids or 0 in human_positions_ids and 4 in human_positions_ids:
                        chosen_place = 'bottom right'

            if chosen_place == '':
                #if still don't know where to go, take a valid random place
                for i in range(len(board.positions)):
                    if board.positions[i].owner == None:
                        chosen_place = board.positions[i].name
                        break

    print('\nThe AI has chosen to put its counter on ' + chosen_place + '.')
    #set the chosen_place's owner to be the AI
    get_position_owner(chosen_place, modify_owner=True)

def choose_place():
    global curr_player

    not_chosen_valid_place = True

    while not_chosen_valid_place:
        chosen_place = raw_input('\n' + curr_player.name + ', where do you choose to put your counter?\nYou can choose from:\n' + get_available_positions(get_pos_names=True))
        chosen_place = chosen_place.lower().strip()

        if chosen_place in get_available_positions(get_pos_names=True) and get_position_owner(chosen_place) == None:
            #set the chosen_place's owner to be the curr_player
            get_position_owner(chosen_place, modify_owner=True)
            not_chosen_valid_place = False

        else:
            print('Invalid choice. Try again.')

def play_again():
    global game_not_endded
    global players
    global curr_player
    global num_draws
    global player_no

    #print stats (current session only)
    if num_draws > 0:
        print('Draws: ' + str(num_draws))
    for i in range(len(players)):
        print('Player ' + str(i+1) + ' wins: ' + str(players[i].num_wins))

    given_invalid_ans = True

    #confirm play again
    while given_invalid_ans:
        play_again_msg = raw_input('\nDo you want to play again?\nChoose from yes and no.\n')
        play_again_msg = re.sub(r'\s+', '', play_again_msg.lower())

        if play_again_msg == 'yes':
            for i in range(len(players)):
                players[i].name = 'Player ' + str(i+1)
                players[i].is_AI = False
                if i%2 == 1:
                    players[i].counter = 'X'
                else:
                    players[i].counter = '0'

            player_no = 0
            curr_player = players[player_no]

            for i in range(len(board.positions)):
                board.positions[i].owner = None

            game_not_endded = True
            play()
            given_invalid_ans = False

        elif play_again_msg == 'no':
            game_not_endded = False
            given_invalid_ans = False

        else:
            print('Invalid option. Try again.')

#main game
def play():
    global game_not_endded
    global curr_player
    global players
    global num_draws

    setup_game_settings()

    while game_not_endded:
        if len(get_available_positions()) > 0:
            board._print()

            if curr_player.is_AI:
                AI_decide_place()

            else:
                choose_place()

            #decide if a player has won
            position_ids = get_positions_by_owner(curr_player, get_ids=True)

            if len(position_ids) > 2:
                #if curr_player has at least 3 positions, carry on checking for if curr_player has won
                #for clarity:
                row_top = [0, 1, 2]
                row_middle = [3, 4, 5]
                row_bottom = [6, 7, 8]
                col_left = [0, 3, 6]
                col_middle = [1, 4, 7]
                col_right = [2, 5, 8]
                di_ltr = [0, 4, 8]
                di_rtl = [2, 4, 6]

                player_has_won = False

                if 0 in position_ids and 1 in position_ids and 2 in position_ids:
                    player_has_won = True#row_top
                if 0 in position_ids and 3 in position_ids and 6 in position_ids:
                    player_has_won = True#col_left
                if 0 in position_ids and 4 in position_ids and 8 in position_ids:
                    player_has_won = True#di_ltr
                if 1 in position_ids and 4 in position_ids and 7 in position_ids:
                    player_has_won = True#col_middle
                if 2 in position_ids and 5 in position_ids and 8 in position_ids:
                    player_has_won = True#col_right
                if 2 in position_ids and 4 in position_ids and 6 in position_ids:
                    player_has_won = True#di_rtl
                if 3 in position_ids and 4 in position_ids and 5 in position_ids:
                    player_has_won = True#row_middle
                if 6 in position_ids and 7 in position_ids and 8 in position_ids:
                    player_has_won = True#row_bottom

                if player_has_won:
                    #if curr_player got valid 3 combo, curr_player has won
                    opponent = players[0]

                    if curr_player == players[0]:
                        opponent = players[1]

                    board._print()
                    print('\nCongratulations, ' + curr_player.name + ', you have defeated ' + opponent.name + '!\n')
                    curr_player.num_wins += 1
                    play_again()

            #let next player take turn
            switch_player()
        else:
            board._print()
            print('\nIt appears that neither of you can choose any more places.\nThis must be a draw.\n')
            num_draws += 1
            play_again()

play()
