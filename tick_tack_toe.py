# This program aims to write an agent for the tick-tack-toe game
# using the minimax algorithm enhanced by alpha-beta pruning.
import sys
sys.setrecursionlimit(1000)
print(sys.getrecursionlimit())
import copy
def judge_value(value)->bool:
    if len(value) != 3: return False
    for i in value:
        if len(i) != 3: return False
        for j in i:
            if j not in 'xo-': return False
    return True

def defaultSymbol(i):
    if i < 3:
        return ('-','x','o')[i]
    return chr(48+i)

class Pos:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
    def __str__(self):
        return f"({self.x},{self.y})"
    def __add__(self, q):
        return Pos(self.x+q.x,self.y+q.y)
    def __sub__(self, q):
        return Pos(self.x-q.x,self.y-q.y)
    def __neg__(self):
        return Pos(-self.x,-self.y)
    def __ge__(self, q):
        return self.x>=q.x and self.y>=q.y
    def __lt__(self, q):
        return self.x<q.x and self.y<q.y
    def __hash__(self):
        return hash((self.x,self.y))
    def copy(self):
        return Pos(self.x, self.y)

_ori = Pos(0,0)


class TickTackToe:
    # The basic setup for the game:
    # m: N of row
    # n: N of col
    # p: N of player
    # s: function: player-id -> symbol
    # sp:function: symbol    -> player-id
    # e: initial symbol
    def __init__(self,m,n,k,p,s=defaultSymbol):
        self.m = m
        self.n = n
        self.k = k
        self.p = p
        self.s = s
        self._borderPoint = Pos(m,n)
        self.values = [[0 for j in range(n)] for i in range(m)]
        # self.lastPlayer = 0
        # self.lastPos = Pos(-1,-1)
        self.posRemaining = set()
        for i in range(m):
            self.posRemaining.update([(i,j) for j in range(n)])
        self.agent_index = 1
        self.history = []
        # 'values' should be a list of m lists, each of which is composed of
        # n values among p kinds of value: 'x','o','-'.
        # An example: [['x','x','o'],['-','o','o'],['x','x','o']]
        # in which 'x'&'o' stand for the occupance of two players,
        # and '-' means that the blank has not yet been occupied.

    # To judge whether the game ends.
    def getPlayer(self,pos:Pos):
        return self.values[pos.x][pos.y]

    def checkSuccess(self):
        if len(self.history) == 0:
            return 0
        def legal(pos:Pos):
            return pos >= _ori and pos < self._borderPoint
        Tr = (Pos(1,0),Pos(0,1),Pos(1,1),Pos(1,-1))
        lastPlayer,lastPos = self.history[-1]
        for tr in Tr:
            counter = 1
            pos = lastPos + tr
            while legal(pos) and self.getPlayer(pos) == lastPlayer:
                counter += 1
                pos = pos + tr
            pos = lastPos - tr
            while legal(pos) and self.getPlayer(pos) == lastPlayer:
                counter += 1
                pos = pos - tr
            if counter >= self.k:
                return lastPlayer
        return 0
        # Tr00 = ((Pos(1,0),Pos(0,1)),(Pos(0,1),Pos(1,0)),(Pos(1,0),Pos(-1,1)),(Pos(0,1),Pos(1,1)))
        # TrM0 = ((Pos(0,1),Pos(-1,1)),(Pos(-1,0),Pos(1,1)))
        # for t1, t2 in Tr00:
        #     start:Pos = Pos(0,0)
        #     while legal(start):
        #         pos = start.copy()
        #         counter = [0 for _ in range(self.p)]
        #         while legal(pos):
        #             player = self.getPlayer(pos)
        #             counter[player]+=1
        #             if counter[player] == self.k:
        #                 return player
        #             pos = pos + t2
        #         start = start + t1
        
    # 1 for 'o' winning, -1 for 'x' winning, 0 for draw or a non-terminal state.

    # To give a score to the game state.
    def score(self,player):
        if self.checkSuccess()==0:
            return 0.5
        return 1 if self.checkSuccess()==player else 0

    # To print the current game state.
    def print_state(self):
        print('The current gameboard:')
        # print('  0 | 1 | 2 ',end='')
        print(f'  0',end='')
        for i in range(1,self.n):
            print(f' | {i}',end='')
        print('\n',end='')
        for i in range(self.m):
            if i > 0:
                print(' ---'+'|---'*(self.n-1))
            print(f'{i} {self.s(self.values[i][0])}',end='')
            for j in range(1,self.n):
                print(f' | {self.s(self.values[i][j])}',end='')
            print('\n',end='')
        # print('0 %s | %s | %s ' % (self.values[0][0], self.values[0][1], self.values[0][2]))
        # print(' ---|---|---')
        # print('1 %s | %s | %s ' % (self.values[1][0], self.values[1][1], self.values[1][2]))
        # print(' ---|---|---')
        # print('2 %s | %s | %s ' % (self.values[2][0], self.values[2][1], self.values[2][2]))
        endStatus = self.checkSuccess()
        if endStatus==0 and len(self.posRemaining) > 0: print('Not ended yet...')
        else:
            print('The game ends!')
            if endStatus == 0:
                print("A draw...")
            else:
                print(f"The winner is Player-{endStatus}!! ({self.s(endStatus)})")
            # match self.is_end()[1]:
            #     case 1: print('Winner: o!!')
            #     case -1: print('Winner: x!!')
            #     case 0: print('A draw...')
        return

    # To generate the possible moves.
    # 'o' moves first.
    # Return a list of where the next move might be.
    # No need to verify whether it is 'o' or 'x' as this is included in self.agent_index.
    def get_legal_moves(self):
        return self.posRemaining
        # if self.is_end()[0]: return None
        # result = []
        # for i in range(3):
        #     for j in range(3):
        #         if self.values[i][j] == '-': result.append([i,j])
        # return result
    def forwardAgentIndex(self):
        if self.agent_index == self.p:
            self.agent_index = 1
        else:
            self.agent_index += 1

    def backwardAgentIndex(self):
        if self.agent_index == 1:
            self.agent_index = self.p
        else:
            self.agent_index -= 1
    
    def move(self,pos:Pos):
        x,y = pos.x, pos.y
        if self.values[x][y] != 0:
            return False
        self.values[x][y] = self.agent_index
        # self.values[x][y] = 'o' if self.agent_index == 0 else 'x'
        self.history.append((self.agent_index,pos))
        self.forwardAgentIndex()
        self.posRemaining.remove((pos.x,pos.y))
        return True
        # self.agent_index = 1 - self.agent_index
    
    def undo(self):
        if len(self.history)!=0:
            self.backwardAgentIndex()
            # self.agent_index = 1 - self.agent_index
            player,pos = self.history.pop()
            self.posRemaining.add((pos.x,pos.y))
            self.values[pos.x][pos.y] = 0
    
    def checkIfEnd(self):
        return self.checkSuccess()!=0 or len(self.posRemaining) == 0

# Def a function, receiving a game: TickTackToe and a move(a point coordinate),
# and return the next new_game: TickTackToe with the target point filled.

# Ahh create a new object!!

# Test code for score assigning and the state printing.
def score_print_test():
    state = [['x','o','-'],['x','o','x'],['o','-','-']]
    game = TickTackToe(state)
    game.print_state()
    print('Legal moves:',game.get_legal_moves()) # Test: get legal moves.
    decision = (0,2)
    game.move(decision)
    game.print_state()

# score_print_test()
'''
The current gameboard:
  0 | 1 | 2 
0 x | o | - 
 ---|---|---
1 x | o | x 
 ---|---|---
2 o | - | - 
Not ended yet...
Legal moves: [[0, 2], [2, 1], [2, 2]]
The current gameboard:
  0 | 1 | 2 
0 x | o | o 
 ---|---|---
1 x | o | x 
 ---|---|---
2 o | - | - 
The game ends!
Winner: o!!
'''
mem = {}

def flat(vals):
    return (item for sublist in vals for item in sublist)
# The alpha-beta pruning minimax agent for the game.
# Return the score of the state and the next move to take according to the agent.
# An example of the next move: (1,2)
def alpha_beta(game:TickTackToe,selfIndex,alpha,beta,depth:9999999):
    # game.print_state()
    # for pos in game.get_legal_moves():
    #     print(pos.__str__(),end=' ')
    # print('')
    # print(list(game.get_legal_moves()))
    if game.checkIfEnd() or depth==0:
        score = game.score(selfIndex) #If it's already terminal state, no need to move.
        return score, None
    
    res = mem.get(flat(game.values))
    if res is not None:
        return res

    legal_actions = game.get_legal_moves()
    if game.agent_index == selfIndex: # It's o turn.Maximizer.
        v = float('-inf')
        best_action = None
        # cnt =0
        for action in legal_actions:
            # if depth==4:
            #     print(f"{cnt}/{len(legal_actions)}")
            #     cnt+=1
            game.move(Pos(action[0],action[1]))
            value,_ = alpha_beta(game,selfIndex,alpha,beta,depth)
            game.undo()
            if value > v:
                v = value
                best_action = action
            if v > beta:
                mem[flat(game.values)] = (v, best_action)
                return v, best_action
            alpha = max(alpha,v)
        mem[flat(game.values)] = (v, best_action)
        return v, best_action

    elif game.agent_index == 3 - selfIndex: # It's x turn.Minimizer.
        v = float('inf')
        best_action = None
        # cnt =0
        for action in legal_actions:
            # if depth==4:
            #     print(f"{cnt}/{len(legal_actions)}")
            #     cnt+=1
            game.move(Pos(action[0],action[1]))
            value,_ = alpha_beta(game,selfIndex,alpha,beta,depth-1)
            game.undo()
            if value < v:
                v = value
                best_action = action
            if v < alpha:
                mem[flat(game.values)] = (v, best_action)
                return v, best_action
            beta = min(beta,v)
        mem[flat(game.values)] = (v, best_action)
        return v, best_action

    else: raise ValueError('Undefined game state!')

# The gaming main function:
def gaming():
    enableSetting = True
    def robotPolicy(player):
        print("I'm a robot. Let me contemplate what to do next!")
        alphabetaResult = alpha_beta(game,player,float('-inf'),float('inf'),7)[1]
        return Pos(alphabetaResult[0],alphabetaResult[1])
    # robotPolicy = lambda game:
    def humanPolicy(player):
        inputStr = input(f"Player {game.agent_index} ({game.s(game.agent_index)})'s move:")
        try:
            inputList = inputStr.split(',')
            return Pos(int(inputList[0]),int(inputList[1]))
        except:
            print("Invalid Move!")
    def getPolicyForAlphaBetaTest(player):
        return [robotPolicy,humanPolicy][player-1]
    def getPolicyRR(player):
        return robotPolicy
    def getPolicyAllHuman(player):
        return humanPolicy
    _allhuman5x6Setting = {"mode":0,"height":5,"width":6,"targetK":4,"playerN":3,"getPolicy":getPolicyAllHuman}
    _tictactoeSetting = {"mode":0,"height":3,"width":4,"targetK":3,"playerN":2,"getPolicy":getPolicyForAlphaBetaTest}
    _5inARow88 = {"mode":0,"height":6,"width":6,"targetK":5,"playerN":2,"getPolicy":getPolicyForAlphaBetaTest}
    # humanPolicy = lambda game:alpha_beta(game,float('-inf'),float('inf'))
    setting = _tictactoeSetting
    if enableSetting:
        mode = setting["mode"]
        height = setting["height"]
        width = setting["width"]
        targetK = setting["targetK"]
        playerN = setting["playerN"]
        print("Using setting. Initializing game with following parameter:")
    else:
        print('This is a tick-tack-toe game, wanting to act first or second?')
        print('type 0 to move first, 1 to move second, 2 to appreciate a robot vs robot display.')
        try:
            mode = int(input('mode choice:'))
            if mode != 0:
                raise ValueError('Illegal game mode! (temporary)')
            if mode != 0 and mode != 1 and mode != 2:
                raise ValueError('Illegal game mode!')
        except:
            raise ValueError('Illegal game mode!')
        height = int(input('input grid height:'))
        width = int(input('input grid width:')) 
        targetK = int(input('input target k:'))
        playerN = int(input('input player number:'))
        print("Well done. Initializing game with following parameter:")
    print(f"mode({mode}) grid: (height={height})x(width={width}) k={targetK} p={playerN}")
    # value = [['-','-','-'],['-','-','-'],['-','-','-']]
    game = TickTackToe(height,width,targetK,playerN)
    print('Every time print the coordinate of your next move.')
    print('For example: to place your move on point(1,2),')
    print('You should type:"1,2"')
    if mode == 2:
        fun_watch()
        return
    while not game.checkIfEnd():
        game.print_state()
        print(f"It's player {game.agent_index}'s move:")
        actionPos = setting["getPolicy"](game.agent_index)(game.agent_index)
        try:
            if not game.move(actionPos):
                print("Invalid Move!")
        except:
            print("Invalid Move!")
        # inputStr = input(f"Player {game.agent_index} ({game.s(game.agent_index)})'s move:")
        # try:
        #     inputList = inputStr.split(',')
        #     # for i in decision_str:
        #     #     if i not in ', ':
        #     #         inputList.append(int(i))
        #     if not game.move(Pos(int(inputList[0]),int(inputList[1]))):
        #         print("Invalid Move!")
        # except:
        #     print("Invalid Move!")
        # if mode == game.agent_index : # It's the player's move!
        #     decision_str = list(input('Your next move:'))
        #     decision = []
        #     for i in decision_str:
        #         if i not in ', ':
        #             decision.append(int(i))
        # else: # It's computer's move!
        #     print("Computer's move!")
        #     a = float('-inf')
        #     b = float('inf')
        #     decision = alpha_beta(game,a,b)[1]
        # game.move(decision)
    game.print_state()
    return


# The robot vs robot:
# Three modes to choose: Rational vs Rational(0); Rational vs random(1); random vs random(2).
def fun_watch():
    print('This is a computer VS computer display.')
    value = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    game = TickTackToe(value)
    while not game.checkSuccess()[0]:
        game.print_state()
        a = float('-inf')
        b = float('inf')
        decision = alpha_beta(game, a, b)[1]
        game.move(decision)
    game.print_state()
    return

gaming()
