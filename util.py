import random

def evaluate(board):
    conflicts = 0
    size = len(board)
    for i in range(size):
        for j in range(i, size):
            # conflicts in row and diagonal
            if i != j and (board[i] == board[j] or j - i == abs(board[i] - board[j])):
                conflicts += 1
    return (size * (size - 1)) / 2 - conflicts


def generate(n):
    return [random.randint(0, n-1) for _ in range(n)]


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print('#' if board[j] == len(board) - 1 - i else '+', end='')
        print()
