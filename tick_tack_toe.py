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
        return True

    # To give a score to the game state.
    def score(self):
        if not self.is_end()[0]: return 0

    # To print the current game state.
    def print_state(self):
        return

# The alpha-beta pruning minimax agent for the game.
def alpha_beta(game:TickTackToe):
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

