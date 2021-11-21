from players import player_exists, get_player_name
from predictions_final import prediction_who_win, prediction_exact, prediction_first_winner
from predictions_final import prediction_extra_point, prediction_total_points


def win_prediction(first_player: str, second_player: str):
    results = prediction_who_win(int(first_player), int(second_player))
    try:
        winner_id = int(results)

        winning_player = get_player_name(str(winner_id))
        prediction = {
            "title": "Winning Player",
            "line1": winning_player
        }
    except ValueError:
        prediction = {
            "title": "Winning Player",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def total_points_prediction(first_player: str, second_player: str):
    results = prediction_total_points(int(first_player), int(second_player))
    try:
        total_points = int(results)
        if total_points == 1:
            prediction = {
                "title": "Total Points",
                "line1": "79 points or more"
            }
        else:
            prediction = {
                "title": "Total Points",
                "line1": "Fewer than 79 points"
            }
    except ValueError:
        prediction = {
            "title": "Total Points",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def number_of_games_prediction(first_player: str, second_player: str):
    results = prediction_exact(int(first_player), int(second_player))
    try:
        number_of_games = int(results)
        prediction = {
            "title": "Number of Games",
            "line1": number_of_games
        }
    except ValueError:
        prediction = {
            "title": "Number of Games",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def first_game_winner_prediction(first_player: str, second_player: str):
    results = prediction_first_winner(int(first_player), int(second_player))
    try:
        first_game_winner = int(results)
        winning_player = get_player_name(str(first_game_winner))
        prediction = {
            "title": "First Game Winner",
            "line1": winning_player
        }
    except ValueError:
        prediction = {
            "title": "First Game Winner",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def games_decided_by_extra_points_prediction(first_player: str, second_player: str):
    results = prediction_extra_point(int(first_player), int(second_player))
    try:
        number_of_games = int(results)
        prediction = {
            "title": "Games Decided By Extra Points",
            "line1": number_of_games
        }
    except ValueError:
        prediction = {
            "title": "Games Decided By Extra Points",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction
