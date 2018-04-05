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
    n = 100000

    hc = HillClimb(size)

    success, boards_searched = hc.run(n, climb_method=HillClimb.find_first_better)
    print('first choice: {:.1f}% success, avg boards checked: {}'.format(success*100, boards_searched))

    success, boards_searched = hc.run(n, climb_method=HillClimb.find_best_child)
    print('steepest ascent: {:.1f}% success, avg boards checked: {}'.format(success*100, boards_searched))

    solutions = 0
    restarts = 0
    progress = tqdm(total=n)
    while solutions < n:
        success, boards_searched = hc.run(1, climb_method=HillClimb.find_first_better)
        restarts += 1
        if success == 1:
            solutions += 1
            progress.update(1)
    progress.close()

    # we're going for n solutions, and the first try for each doesn't count as a restart
    restarts -= n
    print('random restart: {} restarts, avg: {}'.format(restarts, restarts / n))



if __name__ == '__main__':
    main()

