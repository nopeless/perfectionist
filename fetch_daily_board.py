import requests
import numpy as np


# The board dimension specifies whether the board will be returned as a 1d array or 2d array.
# Either way, it will be returned as a Numpy array.
def fetch_daily_board(board_dimension=1):

    response = requests.get("https://louigiverona.com/perfectionist/read_periodicals.php")
    response_body = response.json()

    board = fetch_board(int(response_body[0]), "q")

    if board_dimension == 2:
        return board
    else:
        return board.flatten()


# The board dimension specifies whether the board will be returned as a 1d array or 2d array.
# Either way, it will be returned as a Numpy array.
def fetch_weekly_board(board_dimension=1):
    response = requests.get("https://louigiverona.com/perfectionist/read_periodicals.php")
    response_body = response.json()

    board = fetch_board(int(response_body[1]), "f")

    if board_dimension == 2:
        return board
    else:
        return board.flatten()


# Provide the board seed and the board type.
# By default, board size will be q, or the small daily board size.
# The board seed is required. A 2d Numpy array will be returned for the board.
def fetch_board(board_seed, board_type="q"):

    better_response = requests.post("https://louigiverona.com/perfectionist/add_score.php",
                                    data={"board_seed": board_seed, "board_type": board_type,
                                          "lost": "5", "undo_id_one": "[null]", "undo_id_two": "[null]"})
    rows = better_response.text.split('<br>')[:-1]
    unformatted_board = [row.split('-&')[:-1] for row in rows]
    board = [[int(column[column.find('-') + 1:]) for column in row] for row in unformatted_board]
    return np.array(board)


if __name__ == "__main__":
    print("Testing ... printing the weekly board as a 2d Numpy array:")
    print(fetch_weekly_board(2))
    print()
    print()
    print()
    print("Testing ... printing the daily board as a 1d Numpy array:")
    print(repr(fetch_daily_board()))
