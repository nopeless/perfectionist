import sys
from get_best_fever_score import FeverBoard
import numpy as np
from copy import deepcopy
from fetch_daily_board import fetch_daily_board, fetch_weekly_board, fetch_board

FEVER = 10
RESULTS_FILE = "results.log"
SINGLE_LOSS_MOVE_MAX = 15


class PerfectionistBoard:
    def __init__(self, board):

        self.height = len(board)
        self.width = len(board[0])

        self.size = self.width * self.height

        self.board = board.flatten()
        self.count = np.count_nonzero(self.board)

        self.lost = 0

        self.global_best = sum(self.board)
        self.path = []

    def export_move_sequence(self, moves):
        orig_stdout = sys.stdout
        sys.stdout = open(RESULTS_FILE, "w")
        self_copy = deepcopy(self)
        for i in range(len(moves)):
            print(self_copy)
            self_copy.do_move(moves[i])
        print(self_copy)
        sys.stdout = orig_stdout

    def __repr__(self):
        i = 0
        outstr = "\n" + "-" * (self.width * 3 + 2) + "\n"
        for yy in range(self.height):
            outstr += "|"
            for xx in range(self.width):
                xx, yy
                outstr += str(self.board[i]).rjust(2, " ") + " "
                i += 1
            outstr += "|\n"
        outstr += "-" * (self.width * 3 + 2)
        return outstr

    def do_move(self, move):
        if self.board[move[0]] == self.board[move[1]] and not move[0] == move[1]:
            lost = 0
            self.count -= 2
        else:
            lost = min(self.board[move[1]], self.board[move[0]])
            self.count -= 1
        self.board[move[1]] = abs(self.board[move[1]] - self.board[move[0]])
        self.board[move[0]] = 0
        self.lost += lost
        self.path.append(move)
        return self

    def try_move(self, move):
        self_copy = deepcopy(self)
        if self_copy.board[move[0]] == self_copy.board[move[1]] and not move[0] == move[1]:
            lost = 0
            self_copy.count -= 2
        else:
            lost = min(self_copy.board[move[1]], self_copy.board[move[0]])
            self_copy.count -= 1
        self_copy.board[move[1]] = abs(self_copy.board[move[1]] - self_copy.board[move[0]])
        self_copy.board[move[0]] = 0
        self_copy.lost += lost
        self_copy.path.append(move)
        return self_copy

    def get_good_moves(self):
        available_moves = []
        for row_step in range(0, self.size, self.width):
            for i in range(row_step, row_step + self.width):
                # If the tile is 1, available moves are to match it to all tiles bigger than 1.
                # We probably don't want to match a 1 to another 1.
                if self.board[i] == 1:
                    for j in range(0, self.size):
                        # We probably don't want to match a 1 to another 1.
                        if self.board[j] > 1:
                            available_moves.append((i, j))
                elif self.board[i]:
                    # Look at subsequent tiles in the same row as i
                    for j in range(i + 1, row_step + self.width):
                        if self.board[j] == self.board[i]:
                            available_moves.append((i, j))
                            break
                        elif self.board[j]:
                            loss_value = min(self.board[j], self.board[i])
                            if loss_value <= SINGLE_LOSS_MOVE_MAX:
                                if j != 1:
                                    available_moves.append((j, i))
                                available_moves.append((i, j))
                            break

                    # Look at subsequent tiles in the same column as i
                    for j in range(i + self.width, self.size, self.width):
                        if self.board[j] == self.board[i]:
                            available_moves.append((i, j))
                            break
                        elif self.board[j]:
                            loss_value = min(self.board[j], self.board[i])
                            if loss_value <= SINGLE_LOSS_MOVE_MAX:
                                if j != 1:
                                    available_moves.append((j, i))
                                available_moves.append((i, j))
                            break
        return available_moves

    def evaluate_move(self, move, board_object):
        new_board = board_object.try_move(move)
        move_score = 0
        prev_uses = [move[0], move[1]]
        for board_idx in move:
            tile = new_board.board[board_idx]
            upper_tile = -1
            lower_tile = -1
            left_tile = -1
            right_tile = -1

            for i in range(board_idx % self.width, board_idx, self.width):
                if new_board.board[i] and i not in prev_uses:
                    upper_tile = new_board.board[i]
                    upper_tile_index = i
                    prev_uses.append(i)
            for i in range(board_idx + self.width, self.size, self.width):
                if new_board.board[i]:
                    if i not in prev_uses:
                        lower_tile = new_board.board[i]
                        lower_tile_index = i
                        prev_uses.append(i)
                    break
            for i in range(board_idx + 1, board_idx + (self.width - board_idx % self.width)):
                if new_board.board[i]:
                    if i not in prev_uses:
                        right_tile = new_board.board[i]
                        right_tile_index = i
                        prev_uses.append(i)
                    break
            for i in range((board_idx // self.width) * self.width, board_idx):
                if new_board.board[i] and i not in prev_uses:
                    left_tile = new_board.board[i]
                    left_tile_index = i
                    prev_uses.append(i)

            if tile == upper_tile or tile == lower_tile or tile == right_tile or tile == left_tile:
                move_score += tile
                increase_score = 0
                if upper_tile == tile:
                    increase_score = new_board.evaluate_move([board_idx, upper_tile_index], new_board) - 2 * tile
                elif lower_tile == tile:
                    increase_score = max(increase_score,
                                         new_board.evaluate_move([board_idx, lower_tile_index], new_board) - 2 * tile)
                elif right_tile == tile:
                    increase_score = max(increase_score,
                                         new_board.evaluate_move([board_idx, right_tile_index], new_board) - 2 * tile)
                elif left_tile == tile:
                    increase_score = max(increase_score,
                                         new_board.evaluate_move([board_idx, left_tile_index], new_board) - 2 * tile)
                move_score += increase_score
            if upper_tile == lower_tile and upper_tile != -1 and not tile:
                move_score += upper_tile
                move_score += new_board.evaluate_move([upper_tile_index, lower_tile_index], new_board) - 2 * upper_tile
            if right_tile == left_tile and right_tile != -1 and not tile:
                move_score += right_tile
                move_score += new_board.evaluate_move([left_tile_index, right_tile_index], new_board) - 2 * left_tile
            if tile == 1:
                move_score += 10
        if new_board.lost - board_object.lost == 0:
            move_score += 2 * board_object.board[move[0]]
        move_score -= 4 * (new_board.lost - board_object.lost)

        return move_score

    def evaluate_move_recursively(self, move, breadth, depth, board_object):
        best_score = -1000
        if depth == 0:
            return board_object.evaluate_move(move, board_object)

        new_board = board_object.try_move(move)
        available_moves = new_board.get_good_moves()
        move_scores = \
            [board_object.evaluate_move(move, board_object)
             for move in available_moves]
        moves_indexed_by_evaluation = \
            [x for _, x in sorted(zip(move_scores, available_moves), reverse=True)]
        for next_move in moves_indexed_by_evaluation[:breadth]:
            attempted_score = self.evaluate_move_recursively(next_move, breadth, depth - 1, new_board)
            if attempted_score > best_score:
                best_score = attempted_score
        return best_score + board_object.evaluate_move(move, board_object)

    def attempt_solve(self):
        self.solve_recursively(self)

    def solve_recursively(self, board_object, depth=0):
        # print(depth)
        if board_object.lost < self.global_best:
            if board_object.count <= FEVER:
                # give the Fever Board the remaining nonzero elements from the board for it to solve.
                # This solver leaves it as an exercise to the user to solve once you are in fever.
                best_score = board_object.lost + \
                    FeverBoard(board_object.board[np.nonzero(board_object.board)]). \
                    get_best_fever_score(self.global_best - board_object.lost)
                if best_score < self.global_best:
                    print("New best score found: " + str(best_score))
                    print("Please check the " + RESULTS_FILE + " file for the move sequence")
                    self.export_move_sequence(board_object.path)
                    self.global_best = best_score
                # print("Score found: " + str(best_score))
            else:
                best_score = sum(board_object.board)
                available_moves = board_object.get_good_moves()
                move_scores = \
                    [board_object.evaluate_move(move, board_object)
                     for move in available_moves]
                moves_sorted_by_evaluation = \
                    [x for _, x in sorted(zip(move_scores, available_moves), reverse=True)]
                '''
                if board_object.count >= 16:
                    move_scores = \
                        [board_object.evaluate_move_recursively(move, 5, 2, board_object)
                         for move in moves_sorted_by_evaluation[:5]]
                    moves_sorted_by_evaluation = \
                        [x for _, x in sorted(zip(move_scores, moves_sorted_by_evaluation), reverse=True)]
                '''

                for move in moves_sorted_by_evaluation:
                    new_board = board_object.try_move(move)
                    attempted_score = self.solve_recursively(new_board, depth + 1)
                    if attempted_score < best_score:
                        best_score = attempted_score

        else:
            return 10000
        return best_score


if __name__ == "__main__":
    game_board = fetch_daily_board(2)
    print(game_board)

    my_perf_board = PerfectionistBoard(game_board)
    my_perf_board.attempt_solve()
    #path = [[1, 7], [6, 8], [15, 21], [30, 36], [26, 34], [22, 28], [9, 18], [18, 24], [12, 42], [37, 27], [25, 27], [38, 0], [0, 2], [41, 44], [43, 44], [17, 31], [19, 31], [23, 11], [10, 11], [40, 39], [4, 16], [39, 45], [32, 20], [13, 29], [5, 46], [33, 47], [35, 20], [3, 20], [14, 20]]
    #my_perf_board.export_move_sequence(path)
