# Author: Wilson Ma
# Date: 03/12/2020
# Description: Creates an abstract Xiangqi game with functioning piece specific rules, playing conditions
#              and winning conditions. Players can take turn making moves by specifying coordinates in which they would
#              like their game piece moved.


class XiangqiGame:
    """class represents an abstract xianqi game with board,
        pieces, and winning conditions defined"""

    def __init__(self):
        self._board = [['B-CA', 'B-H', 'B-E', 'B-A', 'B-K', 'B-A', 'B-E', 'B-H', 'B-CA'],
                       ['', '', '', '', '', '', '', '', ''],
                       ['', 'B-CH', '', '', '', '', '', 'B-CH', ''],
                       ['B-S', '', 'B-S', '', 'B-S', '', 'B-S', '', 'B-S'],
                       ['', '', '', '', '', '', '', '', ''],
                       # RIVER
                       ['', '', '', '', '', '', '', '', ''],
                       ['R-S', '', 'R-S', '', 'R-S', '', 'R-S', '', 'R-S'],
                       ['', 'R-CH', '', '', '', '', '', 'R-CH', ''],
                       ['', '', '', '', '', '', '', '', ''],
                       ['R-CA', 'R-H', 'R-E', 'R-A', 'R-K', 'R-A', 'R-E', 'R-H', 'R-CA']
                       # A      B     C      D     E       F       G     H       I
                       ]
        self._game_state = "UNFINISHED"  # initializes game state to unfinished
        self._player_turn = "RED"  # initializes game's starting player to be red
        self._in_check = None

    def get_game_state(self):
        """returns game state status"""
        return self._game_state

    def is_in_check(self, player):
        """method used to check if a player is currently in check"""
        if player == self._in_check:
            return True
        else:
            return False

    def player_turn(self, status):
        """updates player turn to the next player """
        if status == "BLACK":               # indicates which player turn will be next
            self._player_turn = "BLACK"
        if status == "RED":
            self._player_turn = "RED"

    def make_move(self, initial, after):
        """takes the alphabet coordinates converts into numerical value which can
        be used to manipulate the list board"""
        FROM = list(initial)  # converts initial coordinates into a list
        TO = list(after)      # converts after coordinates into a list
        if len(FROM) > 2:     # converts two digits notations into single, ie a10
            FROM[1] = FROM[1] + FROM[2]
            FROM.pop(2)
        if len(TO) > 2:
            TO[1] = TO[1] + TO[2]
            TO.pop(2)
        if 'a' in FROM:         # converts from a - i into 0-8
            FROM[0] = 0
        if 'b' in FROM:
            FROM[0] = 1
        if 'c' in FROM:
            FROM[0] = 2
        if 'd' in FROM:
            FROM[0] = 3
        if 'e' in FROM:
            FROM[0] = 4
        if 'f' in FROM:
            FROM[0] = 5
        if 'g' in FROM:
            FROM[0] = 6
        if 'h' in FROM:
            FROM[0] = 7
        if 'i' in FROM:
            FROM[0] = 8
        if 'a' in TO:
            TO[0] = 0
        if 'b' in TO:
            TO[0] = 1
        if 'c' in TO:
            TO[0] = 2
        if 'd' in TO:
            TO[0] = 3
        if 'e' in TO:
            TO[0] = 4
        if 'f' in TO:
            TO[0] = 5
        if 'g' in TO:
            TO[0] = 6
        if 'h' in TO:
            TO[0] = 7
        if 'i' in TO:
            TO[0] = 8
        return XiangqiGame.make_move_helper(self, (10 - int(FROM[1])), int(FROM[0]), 10 - int(TO[1]), int(TO[0]))

    def make_move_helper(self, row_from, column_from, row_to, column_to):
        """takes the coordinates from and to, uses them to move the pieces on the board"""

        if self._board[row_from][column_from] == '':  # returns false if board coordinates does not contain a piece
            return False
        if row_from > 9 or row_from < -1 or row_to > 9 or column_to < -1:  # out of bounds check
            return False
        if self._game_state != "UNFINISHED":  # checks to see if game has already been won or not
            return False

        # RED PLAYER PIECES
        if self._player_turn == "RED" and 'R-' in self._board[row_from][column_from]:  # checks if its reds turn and are red's pieces

            # SOLDIER
            if 'R-S' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][
                    column_to]:
                if row_from > 4:  # checks to see if soldier is behind river
                    if self._board[column_from] == self._board[column_to] and row_from > row_to and \
                            row_to - row_from == -1:  # can only move 1 space ahead
                        self._board[row_to][column_to] = 'R-S'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from < 5:
                    if row_to - row_from == -1:  # if piece is across the river
                        if self._board[column_from] == self._board[column_to]:  # 1 move ahead
                            self._board[row_to][column_to] = 'R-S'
                            self._board[row_from][column_from] = ''
                        if self._board[row_to - 1][column_to] == 'B-K':
                            self._in_check = "black"
                            return XiangqiGame.player_turn(self, "BLACK"), True
                        else:
                            return XiangqiGame.player_turn(self, "BLACK"), True
                    if row_to == row_from:
                        if column_to - column_from == 1 or column_to - column_from == -1:# allows soldier to move horizontal
                            self._board[row_to][column_to] = 'R-S'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True

            # CANNON
            if 'R-CA' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                count = 1
                if column_from == column_to and row_from < row_to:
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:  # checks if any pieces blocking forward
                            return False
                        count += 1                                      # iterates through the list to check for blocks
                    self._board[row_to][column_to] = 'R-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if column_from == column_to and row_from > row_to:
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:  # checks if any pieces blocking backwards
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from == row_to and column_from > column_to:  # checks if any pieces blocking left
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from == row_to and column_from < column_to:  # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True

            # ELEPHANT
            if 'R-E' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                if row_from > 4:
                    if row_from-row_to == 2 and column_from - column_to == 2:
                        if '-' not in self._board[row_from-1][column_from - 1]:     # no blocks upper left
                            self._board[row_to][column_to] = 'R-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True
                        else:
                            return False
                    if row_to - row_from == 2 and column_to - column_from == 2:  # no blocks lower right
                        if '-' not in self._board[row_from + 1][column_from + 1]:
                            self._board[row_to][column_to] = 'R-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True
                        else:
                            return False
                    if row_from - row_to == 2 and column_to - column_from == 2:    # no blocks upper right
                        if '-' not in self._board[row_from - 1][column_from + 1]:
                            self._board[row_to][column_to] = 'R-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True
                        else:
                            return False
                    if row_to - row_from == 2 and column_from - column_to == 2:    # no blocks lower left
                        if '-' not in self._board[row_from + 1][column_from - 1]:
                            self._board[row_to][column_to] = 'R-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True
                        else:
                            return False

            # GENERAL
            if 'R-K' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                if row_from == row_to:
                    if column_from-column_to == 1 or column_from - column_to == -1:
                        if [row_to, column_to] == [9, 4] or [row_to, column_to] == [9, 3] or [row_to, column_to] == [9, 5] \
                                or [row_to, column_to] == [8, 3] or [row_to, column_to] == [8, 4] or [row_to, column_to] == [8, 5] \
                                or [row_to, column_to] == [7, 3] or [row_to, column_to] == [7, 4] or [row_to, column_to] == [7, 5]:
                            self._board[row_to][column_to] = 'R-K'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True
                if row_to != row_from:
                    if column_from == column_to:
                        if [row_to, column_to] == [9, 4] or [row_to, column_to] == [9, 3] or [row_to, column_to] == [9,5] \
                                or [row_to, column_to] == [8, 3] or [row_to, column_to] == [8, 4] or [row_to,column_to] == [8,5] \
                                or [row_to, column_to] == [7, 3] or [row_to, column_to] == [7, 4] or [row_to,column_to] == [7,5]:
                            self._board[row_to][column_to] = 'R-K'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "BLACK"), True

            # ADVISOR
            if 'R-A' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                if column_to - column_from == 1 or column_to - column_from == -1:
                    if [row_to, column_to] == [7, 3] or [row_to, column_to] == [7, 5] or [row_to, column_to] == [8, 4] \
                            or [row_to, column_to] == [9, 3] or [row_to, column_to] == [9, 5]:
                        self._board[row_to][column_to] = 'R-A'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True

            # HORSE
            if 'R-H' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                if row_from - row_to == 2 and column_to - column_from == 1:   #moving horse top left and checks for blocking
                    if '-' not in self._board[row_from - 1][column_to - 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from - row_to == 2 and column_from - column_to == 1:  #moving horse top right and checks for blocking
                    if '-' not in self._board[row_from - 1][column_to + 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_to - row_from == 2 and column_from - column_to == 1:  # moves the horse lower left
                    if '-' not in self._board[row_from + 1][column_to + 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_to - row_from == 2 and column_to - column_from == 1:  # moves the horse lower right
                    if '-' not in self._board[row_from + 1][column_to - 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_to - row_from == 1 and column_to - column_from == 2:  # moves the horse right lower
                    if '-' not in self._board[row_from][column_to - 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from - row_to == 1 and column_to - column_from == 2:  # moves the horse right upper
                    if '-' not in self._board[row_from][column_to - 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from - row_to == 1 and column_from - column_to == 2:  # moves the horse left upper
                    if '-' not in self._board[row_from][column_to + 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
                if row_to - row_from == 1 and column_from - column_to == 2: # moves the horse left lower,checks blockage
                    if '-' not in self._board[row_from][column_to + 1]:
                        self._board[row_to][column_to] = 'R-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True

            # CHARIOT
            if 'R-CH' in self._board[row_from][column_from] and 'B-' in self._board[row_to][column_to]:
                if column_from == column_to and row_from > row_to:
                    count = 1               # forward movement capture
                    piece = 0               # initializes piece count to see if chariot can capture
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:
                            count += 1
                            piece += 1      # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    print(piece)
                    if piece == 2:
                        self._board[row_to][column_to] = 'R-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
            if 'R-CH' in self._board[row_from][column_from] and 'B-' in self._board[row_to][column_to]:
                if column_from == column_to and row_from < row_to:
                    count = 1                                   # backward movement capture
                    piece = 0
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:
                            count += 1
                            piece += 1                           # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'R-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
            if 'R-CH' in self._board[row_from][column_from] and 'B-' in self._board[row_to][column_to]:
                if row_from == row_to and column_from > column_to:
                    count = 1                                   # left movement capture
                    piece = 0
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            count += 1
                            piece += 1                           # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'R-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
            if 'R-CH' in self._board[row_from][column_from] and 'B-' in self._board[row_to][column_to]:
                if row_from == row_to and column_from < column_to:
                    count = 1                                   # right movement capture
                    piece = 0                                     # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            count += 1
                            piece += 1                           # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'R-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "BLACK"), True
            if 'R-CH' in self._board[row_from][column_from] and 'R-' not in self._board[row_to][column_to]:
                count = 1
                if column_from == column_to and row_from < row_to:
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:  # checks if any pieces blocking backwards
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if column_from == column_to and row_from > row_to:
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:  # checks if any pieces blocking forward
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from == row_to and column_from > column_to:  # checks if any pieces blocking left
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
                if row_from == row_to and column_from < column_to:  # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'R-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "BLACK"), True
            else:
                return False

        # BLACK PLAYER PIECES
        if self._player_turn == "BLACK" and 'B-' in self._board[row_from][column_from]:  # checks if its black's turn and are black's pieces

            # SOLDIER
            if 'B-S' in self._board[row_from][column_from]:
                if row_from < 5:  # checks to see if soldier is behind river
                    if self._board[column_from] == self._board[column_to] and row_from < row_to and \
                            row_to - row_from == 1:  # can only move 1 space ahead
                        self._board[row_to][column_to] = 'B-S'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
            if row_from > 4:  # if soldier has already crossed the river
                if row_from - row_to == -1:
                    if self._board[column_from] == self._board[column_to]:
                        self._board[row_to][column_to] = 'B-S'
                        self._board[row_from][column_from] = ''
                    if self._board[row_to + 1][column_to] == 'B-K' or self._board[row_to][column_to - 1] == 'B-K' \
                            or self._board[row_to][column_to + 1] == 'B-K':
                        self._in_check = "red"
                        return XiangqiGame.player_turn(self, "RED"), True
                    else:
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_to == row_from:  # soldier can move 1 space horizontally in the row
                    if column_to - column_from == 1 or column_to - column_from == -1:
                        self._board[row_to][column_to] = 'B-S'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True

            # CANNON
            if 'B-CA' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                count = 1
                if column_from == column_to and row_from < row_to:
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:  # checks if any pieces blocking forward
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if column_from == column_to and row_from > row_to:
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:  # checks if any pieces blocking backwards
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if row_from == row_to and column_from > column_to:              # checks if any pieces blocking left
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if row_from == row_to and column_from < column_to:               # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CA'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True

            # ELEPHANT
            if 'B-E' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                if row_from < 5:
                    if row_from - row_to == 2 and column_from - column_to == 2:
                        if '-' not in self._board[row_from - 1][column_from - 1]:  # no blocks upper left
                            self._board[row_to][column_to] = 'B-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "RED"), True
                        else:
                            return False
                    if row_to - row_from == 2 and column_to - column_from == 2:  # no blocks lower right
                        if '-' not in self._board[row_from + 1][column_from + 1]:
                            self._board[row_to][column_to] = 'B-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "RED"), True
                        else:
                            return False
                    if row_from - row_to == 2 and column_to - column_from == 2:  # no blocks upper right
                        if '-' not in self._board[row_from - 1][column_from + 1]:
                            self._board[row_to][column_to] = 'B-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "RED"), True
                        else:
                            return False
                    if row_to - row_from == 2 and column_from - column_to == 2:  # no blocks lower left
                        if '-' not in self._board[row_from + 1][column_from - 1]:
                            self._board[row_to][column_to] = 'B-E'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "RED"), True
                        else:
                            return False

            # GENERAL
            if 'B-K' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                if row_from == row_to:
                    if column_from-column_to == 1 or column_from - column_to == -1:
                        if [row_to, column_to] == [0, 4] or [row_to, column_to] == [0, 3] or [row_to, column_to] == [0, 5] \
                                or [row_to, column_to] == [1, 3] or [row_to, column_to] == [1, 4] or [row_to,column_to] == [1, 5] \
                                or [row_to, column_to] == [2, 3] or [row_to, column_to] == [2, 4] or [row_to,column_to] == [2, 5]:
                            self._board[row_to][column_to] = 'B-K'
                            self._board[row_from][column_from] = ''
                            return XiangqiGame.player_turn(self, "RED"), True
                if row_to != row_from:
                    if column_from == column_to:
                        if row_from - row_to == 1 or row_from - row_to ==-1:
                            if [row_to, column_to] == [0, 4] or [row_to, column_to] == [0, 3] or [row_to, column_to] == [0, 5] \
                                    or [row_to, column_to] == [1, 3] or [row_to, column_to] == [1, 4] or [row_to,column_to] == [1, 5] \
                                    or [row_to, column_to] == [2, 3] or [row_to, column_to] == [2, 4] or [row_to,column_to] == [2, 5]:
                                self._board[row_to][column_to] = 'B-K'
                                self._board[row_from][column_from] = ''
                                return XiangqiGame.player_turn(self, "RED"), True

            # ADVISOR
            if 'B-A' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                if column_to - column_from == 1 or column_to - column_from == -1:
                    if [row_to, column_to] == [0, 3] or [row_to, column_to] == [0, 5] or [row_to, column_to] == [2, 3] \
                            or [row_to, column_to] == [1, 4] or [row_to, column_to] == [2, 5]:
                        self._board[row_to][column_to] = 'B-A'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True

            # HORSE
            if 'B-H' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                if row_from - row_to == 2 and column_to - column_from == 1:  # moving horse top left and checks for blocking
                    if '-' not in self._board[row_from - 1][column_to - 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_from - row_to == 2 and column_from - column_to == 1:  # moving horse top right and checks for blocking
                    if '-' not in self._board[row_from - 1][column_to + 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_to - row_from == 2 and column_from - column_to == 1:  # moves the horse lower left
                    if '-' not in self._board[row_from + 1][column_to + 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_to - row_from == 2 and column_to - column_from == 1:  # moves the horse lower right
                    if '-' not in self._board[row_from + 1][column_to - 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_to - row_from == 1 and column_to - column_from == 2:  # moves the horse right lower
                    if '-' not in self._board[row_from][column_to - 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_from - row_to == 1 and column_to - column_from == 2:  # moves the horse right upper
                    if '-' not in self._board[row_from][column_to - 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_from - row_to == 1 and column_from - column_to == 2:  # moves the horse left upper
                    if '-' not in self._board[row_from][column_to + 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
                if row_to - row_from == 1 and column_from - column_to == 2:  # moves the horse left lower,checks blockage
                    if '-' not in self._board[row_from][column_to + 1]:
                        self._board[row_to][column_to] = 'B-H'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True

            # CHARIOT
            if 'B-CH' in self._board[row_from][column_from] and 'R-' in self._board[row_to][column_to]:
                if column_from == column_to and row_from > row_to:
                    count = 1  # forward movement capture
                    piece = 0  # initializes piece count to see if chariot can capture
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:
                            count += 1
                            piece += 1  # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    print(piece)
                    if piece == 2:
                        self._board[row_to][column_to] = 'B-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
            if 'B-CH' in self._board[row_from][column_from] and 'R-' in self._board[row_to][column_to]:
                if column_from == column_to and row_from < row_to:
                    count = 1  # backward movement capture
                    piece = 0
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:
                            count += 1
                            piece += 1  # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'B-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
            if 'B-CH' in self._board[row_from][column_from] and 'R-' in self._board[row_to][column_to]:
                if row_from == row_to and column_from > column_to:
                    count = 1  # left movement capture
                    piece = 0
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            count += 1
                            piece += 1  # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'B-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
            if 'B-CH' in self._board[row_from][column_from] and 'R-' in self._board[row_to][column_to]:
                if row_from == row_to and column_from < column_to:
                    count = 1  # right movement capture
                    piece = 0  # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            count += 1
                            piece += 1  # counts how many "pieces" between target and chariot
                        else:
                            count += 1
                    if piece == 2:
                        self._board[row_to][column_to] = 'B-CH'
                        self._board[row_from][column_from] = ''
                        return XiangqiGame.player_turn(self, "RED"), True
            if 'B-CH' in self._board[row_from][column_from] and 'B-' not in self._board[row_to][column_to]:
                count = 1
                if column_from == column_to and row_from < row_to:
                    for num in range(row_to - row_from):
                        if '-' in self._board[row_from + count][column_from]:  # checks if any pieces blocking backwards
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if column_from == column_to and row_from > row_to:
                    for num in range(row_from - row_to):
                        if '-' in self._board[row_from - count][column_from]:  # checks if any pieces blocking forward
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if row_from == row_to and column_from > column_to:  # checks if any pieces blocking left
                    for num in range(column_from - column_to):
                        if '-' in self._board[row_from][column_from - count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
                if row_from == row_to and column_from < column_to:  # checks if any pieces blocking right
                    for num in range(column_to - column_from):
                        if '-' in self._board[row_from][column_from + count]:
                            return False
                        count += 1
                    self._board[row_to][column_to] = 'B-CH'
                    self._board[row_from][column_from] = ''
                    return XiangqiGame.player_turn(self, "RED"), True
            else:
                return False

