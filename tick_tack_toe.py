# This program aims to write an agent for the tick-tack-toe game
# using the minimax algorithm enhanced by alpha-beta pruning.

def judge_value(value)->bool:
    if len(value) != 3: return False
    for i in value:
        if len(i) != 3: return False
        for j in i:
            if j not in 'xo-': return False
    return True

class TickTackToe:
    # The basic setup for the game:
    def __init__(self,values):
        self.values = values
        # 'values' should be a list of three lists, each of which is composed of
        # three values among 'x','o','-'.
        # An example: [['x','x','o'],['-','o','o'],['x','x','o']]
        # in which 'x'&'o' stand for the occupance of two players,
        # and '-' means that the blank has not yet been occupied.
        if not judge_value(self.values):
            raise ValueError('Not an eligible value!')

    # To judge whether the game ends.
    def is_end(self):
        for i in self.values:
            if i[0] == i[1] == i[2] == 'o':return True,1
            if i[0] == i[1] == i[2] == 'x':return True,-1
        for column_index in range(3):
            if self.values[0][column_index] == self.values[1][column_index] == self.values[2][column_index] == 'o':
                return True,1
            if self.values[0][column_index] == self.values[1][column_index] == self.values[2][column_index] == 'o':
                return True,-1
        if self.values[0][0] == self.values[1][1] == self.values[2][2] == 'o':return True,1
        if self.values[0][0] == self.values[1][1] == self.values[2][2] == 'x': return True,-1
        if self.values[0][2] == self.values[1][1] == self.values[2][0] == 'o': return True, 1
        if self.values[0][2] == self.values[1][1] == self.values[2][0] == 'x': return True,-1
        for i in range(3):
            for j in range(3):
                if self.values[i][j] == '-':return False,0
        return True,0
    # 1 for 'o' winning, -1 for 'x' winning, 0 for draw or a non-terminal state.

    # To give a score to the game state.
    def score(self):
        return self.is_end()[1]

    # To print the current game state.
    def print_state(self):
        print('The current gameboard:')
        print(' %s | %s | %s ' % (self.values[0][0], self.values[0][1], self.values[0][2]))
        print('---|---|---')
        print(' %s | %s | %s ' % (self.values[1][0], self.values[1][1], self.values[1][2]))
        print('---|---|---')
        print(' %s | %s | %s ' % (self.values[2][0], self.values[2][1], self.values[2][2]))
        if not self.is_end()[0]: print('Not ended yet...')
        else:
            print('The game ends!')
            match self.is_end()[1]:
                case 1: print('Winner: o!!')
                case -1: print('Winner: x!!')
                case 0: print('A draw...')
        return

    # To generate the possible states after the next move.
    # 'o' moves first.
    def generate_successor(self):
        if self.is_end(): return None
        o_count = 0 ; x_count = 0
        for i in range(3):
            for j in range(3):
                match self.values[i][j]:
                    case 'x' : x_count += 1
                    case 'o' : o_count += 1
        if o_count == x_count or o_count == x_count + 1:
            ...
        else:
            raise ValueError('Not a possible tick-tack-toe state!')
        return None

# Test code for score assigning and the state printing.
def score_print_test():
    state = [['x','x','o'],['-','o','x'],['o','x','o']]
    game = TickTackToe(state)
    game.print_state()

#score_print_test()

# The alpha-beta pruning minimax agent for the game.
# Return the score of the state and the next move to take according to the agent.
# Agent index: 1 for 'o'; '-1' for 'x'.
def alpha_beta(agent_index,game:TickTackToe,alpha,beta):
    if game.is_end():
        return game.score(),None #If it's already terminal state, no need to move.


    return

# The gaming main function:
def gaming():
    return

# The robot vs robot:
# Three modes to choose: Rational vs Rational(0); Rational vs random(1); random vs random(2).
def fun_watch(mode_code: int):
    if mode_code not in range(2):
        raise ValueError('An invalid mode code!')
    return

