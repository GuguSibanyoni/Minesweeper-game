import random
import re

# board object
class Board:

    def __init__(self, dimension_size, num_bombs):
        self.dimension_size = dimension_size
        self.num_bombs = num_bombs

        # creating the board and helper function
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # The set is there to keep track of which locations we have uncovered by saving (row,col) tuples into this set
        self.dug = set()

    def make_new_board(self):

        # generating a new board
        board = [[None for _ in range(self.dimension_size)] for _ in range(self.dimension_size)]


        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dimension_size ** 2 - 1)
            row = loc // self.dimension_size
            col = loc % self.dimension_size

            if board[row][col] == '*':
                # this means we have already planted a bomb there so keep going
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dimension_size):
            for c in range(self.dimension_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # we iterate through each of the neighboring positions and sum number of bombs

        num_neighboring_bombs = 0
        for i in range(max(0, row - 1), min(self.dimension_size - 1, row + 1) + 1):
            for j in range(max(0, col - 1), min(self.dimension_size - 1, col + 1) + 1):
                if i == row and j == col:
                    continue
                if self.board[i][j] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dimension_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dimension_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug, if our initial dig didn't dig a bomb, we wouldn't dig one here
                self.dig(r, c)

        return True

    def __str__(self):

        visible_board = [[None for _ in range(self.dimension_size)] for _ in range(self.dimension_size)]
        for row in range(self.dimension_size):
            for col in range(self.dimension_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        widths = []
        for i in range(self.dimension_size):
            columns = map(lambda x: x[i], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dimension_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimension_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play_game(dimension_size=10, num_bombs=10):
    board = Board(dimension_size, num_bombs)
    safe = True

    while len(board.dug) < board.dimension_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dimension_size or col < 0 or col >= dimension_size:
            print("Invalid location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            # dug a bomb, game over
            break

    if safe:
        print("CONGRATULATIONS!!!! YOU WON!")
    else:
        print("SORRY GAME OVER :(")
        board.dug = [(r, c) for r in range(board.dimension_size) for c in range(board.dimension_size)]
        print(board)


if __name__ == '__main__':
    play_game()