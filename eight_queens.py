# This program tries to construct different algorithms for the eight_queen problems.
# Namely, I aim to realize the iterative algorithm and the genetic algorithm.

# The variables: The position of the n queens.
# The domain: The points in the n*n grid.
# The constraints: Any two queens cannot attack each other.

import random
import copy
import math

# A function that judges whether two queens can attack each other.
def judge(xy1:list,xy2:list)->bool:
    assert len(xy1)==2 and len(xy2)==2
    try:
        return False if xy1[0]==xy2[0] or xy1[1]==xy2[1] or xy1[1]-xy2[1]==xy1[0]-xy2[0] or xy1[1]-xy2[1]==-xy1[0]+xy2[0] else True
    except:
        raise ValueError('Not two valid points input.')

class QueensProblem:
    def __init__(self, number, values):
        self.number = number
        # Values assigned (provisionally).
        # 'values' shall be a list of n point coordinates, which are stored as two-dimension lists.
        self.values = values
        if len(values) != number:
            raise ValueError('Not enough values assigned!')

    def shallow_copy(self):
        return QueensProblem(self.number,self.values)

    def heuristic(self)->int:
        conflicts = 0
        for i in self.values:
            for j in self.values:
                if i != j and judge(i,j) == False: conflicts += 1
        return conflicts

    def is_aim(self):
        return self.heuristic() == 0

    def print_answer(self)->None:
        for i in range(self.number):
            for j in range(self.number):
                if [i,j] in self.values: print('Q',end='    ')
                else: print('x',end='    ')
            print('\n')

    # For the sake of iterable algorithm, get the list of values, including the current values:
    def successors(self):
        adjacent = []
        # The first layer is to iterate between the value to change.
        for i in range(self.number):
            # Important! Only change the position of a queen if it violates a constraint.
            change = False
            for j in range(self.number):
                if i != j:
                    if not judge(self.values[i],self.values[j]):
                        change = True
                        break
            if change:
                # The second layer is to iterate between the new value, only allowing it to change within the column.
                for j in range(self.number):
                    if self.values[i] != [i, j]:
                        new_value = copy.deepcopy(self.values)
                        new_value[i] = [i, j]
                        adjacent.append(new_value)
        return adjacent

# To generate the initial random value assignment for either algorithm.
def queen_initialize(size:int):
    initial_values = []
    for column in range(size):
        initial_values.append([column,random.randint(0,size-1)])
    return initial_values

# iterative algorithm for the queen problem
# accept a problem and its state of values, return the problem with its new state of value.

# Local search can have problem! Introduce simulate annealing!

def accept_probability(heuristic_difference,iterate_time):
    # For more complicated problems, division temperature may decrease too fast,
    # in which case we may introduce exponential temperature.
    temperature = 1/(1+(iterate_time/1000))
    return math.e**(heuristic_difference/temperature)

# Return 1 with the given probability, else return 0.
def if_accept(probability)->bool:
    return random.random() < probability

def iterative(problem:QueensProblem):
    result = problem.shallow_copy()
    iterate_time = 0
    while not result.is_aim():
        if iterate_time>50000:
            print('Last trial:')
            result.print_answer()
            raise RuntimeError('Oops...No solution found after careful search...')
        scores = []
        for moves in result.successors():
            moves_problem = QueensProblem(problem.number,moves)
            scores.append(moves_problem.heuristic())
        minimum = min(scores)

        '''
        # This method doesn't use simulating annealing, which can cause problems in some cases.
        min_list = []
        for i,score in enumerate(scores):
            if score == minimum: min_list.append(i)
        min_index = random.choice(min_list)
        result.values = result.successors()[min_index]
        '''

        accept_list = []
        for i, score in enumerate(scores):
            if score == minimum or if_accept(accept_probability(minimum-score,iterate_time)):accept_list.append(i)
        choose_index = random.choice(accept_list)
        result.values = result.successors()[choose_index]
        iterate_time += 1
    return result

# The main function for the iterable algorithm.
def main_ite():
    try:
        size = int(input('The size of the queen problem:'))
        if size <= 3:
            raise ValueError('Size>3 for soluble queens problem.')
    except:
        raise ValueError('An invalid size!')
    problem = QueensProblem(size,queen_initialize(size))
    solution = iterative(problem)
    solution.print_answer()

# Check if the algorithm is strong enough.
def checker(trial_time):
    problem = QueensProblem(8, queen_initialize(8))
    success_time = 0
    for i in range(trial_time):
        try:
            solution = iterative(problem)
            success_time += 1
        except RuntimeError:
            ...
    print('Success %i times in %i'%(success_time,trial_time))
    return

'''
checker(1000)
'''

main_ite()

