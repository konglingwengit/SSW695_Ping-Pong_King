from players import player_exists, get_player_name
from machine_learning.Predictor import predict_winner


def win_prediction(first_player: str, second_player: str):
    results = predict_winner(int(first_player), int(second_player))
    if 'winner_id' in results and 'win_chance' in results:
        winning_player = get_player_name(str(results['winner_id']))
        prediction = {
            "title": "Winning Player",
            "line1": winning_player,
            "line2": "Probability: " + str(results['win_chance'])
        }
        if 'confidence' in results:
            prediction['line3'] = "With " + results['confidence'] + " confidence"
    else:
        prediction = {
            "title": "Winning Player",
            "line1":  "Prediction Failed",
        }
    return prediction


def total_points_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        total_points = 33 + int(first_player) * 7 + int(second_player) * 4
        prediction = {
            "title": "Total Points",
            "line1": total_points
        }
    else:
        prediction = {
            "title": "Total Points",
            "line1": "Invalid player ID(s): requested " + first_player + " and " + second_player
        }
    return prediction


def number_of_games_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        skill_difference = abs(int(first_player) - int(second_player))
        if skill_difference > 3:
            number_of_games = 3
        elif skill_difference > 2:
            number_of_games = 4
        else:
            number_of_games = 5
        prediction = {
            "title": "Number of Games",
            "line1": number_of_games
        }
    else:
        prediction = {
            "title": "Number of Games",
            "line1": "Invalid player ID(s): requested " + first_player + " and " + second_player
        }
    return prediction


def third_game_winner_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        if int(first_player) + 1 < int(second_player):
            winning_player = get_player_name(first_player)
        else:
            winning_player = get_player_name(second_player)
        prediction = {
            "title": "Third Game Winner",
            "line1": winning_player
        }
    else:
        prediction = {
            "title": "Third Game Winner",
            "line1": "Invalid player ID(s): requested " + first_player + " and " + second_player
        }
    return prediction


def games_decided_by_extra_points_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        skill_difference = abs(int(first_player) - int(second_player))
        if skill_difference > 3:
            number_of_games = 0
        elif skill_difference > 2:
            number_of_games = 1
        else:
            number_of_games = 2
        prediction = {
            "title": "Games Decided By Extra Points",
            "line1": number_of_games
        }
    else:
        prediction = {
            "title": "Games Decided By Extra Points",
            "line1": "Invalid player ID(s): requested " + first_player + " and " + second_player
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
