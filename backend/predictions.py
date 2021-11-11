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
    except:
        prediction = {
            "title": "Winning Player",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def total_points_prediction(first_player: str, second_player: str):
    results = prediction_total_points(int(first_player), int(second_player))
    try:
        total_points = int(results)
        prediction = {
            "title": "Total Points",
            "line1": total_points
        }
    except:
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
    except:
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
    except:
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
    except:
        prediction = {
            "title": "Games Decided By Extra Points",
            "line1": "Prediction Failed with message " + str(results)
        }
    return prediction


def money_line_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        skill_difference = abs(int(first_player) - int(second_player))

        if skill_difference > 1000:
            player1_money = "+ 100"
            player2_money = "- 200"
        else:
            player1_money = "- 50"
            player2_money = "- 150"

        player1 = get_player_name(first_player)
        player2 = get_player_name(second_player)

        prediction = {
            "title": "Money Line",
            "line1": player1 + ": " + player1_money,
            "line2": player2 + ": " + player2_money
        }
    else:
        prediction = {
            "title": "Money Line",
            "line1": "Invalid player ID(s): requested " + first_player + " and " + second_player
        }
    return prediction
