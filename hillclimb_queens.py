#!/usr/bin/env python

from util import generate, evaluate, print_board
try:
    from tqdm import tqdm
except:
    def tqdm(x):
        return x


def expand(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            yield board[:i] + [(board[i] + j) % size] + board[i+1:]


class HillClimb:
    def __init__(self, size):
        self.size = size
        self.max_fitness = (size * (size - 1)) / 2

    def run(self, n, climb_method):
        self.boards_searched = 0
        solved = 0

        for i in tqdm(range(n)):
            board = generate(self.size)
            f = evaluate(board)
            previous_f = f - 1
            while previous_f < f:
                previous_f = f
                board, f = climb_method(self, board)
            if f == self.max_fitness:
                solved += 1
        return solved/n, self.boards_searched/n


    def find_first_better(self, board):
        f = evaluate(board)
        for child in expand(board):
            child_f = evaluate(child)
            self.boards_searched += 1
            if child_f > f:
                return child, child_f
        return board, f
        

    def find_best_child(self, board):
        best_child = board
        best_f = evaluate(board)
        for child in expand(board):
            child_f = evaluate(child)
            self.boards_searched += 1
            if child_f > best_f:
                best_f = child_f
                best_child = child
        return best_child, best_f


def main():
    size = 8
    n = 1000

    hc = HillClimb(size)

    success, boards_searched = hc.run(n, climb_method=HillClimb.find_first_better)
    print('first choice: {}% success, avg boards checked: {}'.format(int(success*100), boards_searched))

    success, boards_searched = hc.run(n, climb_method=HillClimb.find_best_child)
    print('steepest ascent: {}% success, avg boards checked: {}'.format(int(success*100), boards_searched))

if __name__ == '__main__':
    main()

