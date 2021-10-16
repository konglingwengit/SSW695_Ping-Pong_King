from players import player_exists, get_player_name


def win_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        if second_player < first_player:
            winner_id = second_player
        else:
            winner_id = first_player
        winning_player = get_player_name(winner_id)
        win_chance = 0.75
        prediction = {
            "winner_name": winning_player,
            "winner_id": winner_id,
            "win_chance": win_chance
        }
        return prediction
    else:
        return "Invalid player ID(s): requested " + first_player + " and " + second_player


def total_points_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        total_points = 33 + int(first_player) * 7 + int(second_player) * 4
        prediction = {
            "total_points": total_points
        }
        return prediction
    else:
        return "Invalid player ID(s): requested " + first_player + " and " + second_player


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
            "number_of_games": number_of_games
        }
        return prediction
    else:
        return "Invalid player ID(s): requested " + first_player + " and " + second_player


def third_game_winner_prediction(first_player: str, second_player: str):
    if player_exists(first_player) and player_exists(second_player):
        if int(first_player) + 1 < int(second_player):
            winning_player = get_player_name(first_player)
        else:
            winning_player = get_player_name(second_player)
        prediction = {
            "third_game_winner": winning_player
        }
        return prediction
    else:
        return "Invalid player ID(s): requested " + first_player + " and " + second_player


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
            "games_decided_by_extra_points": number_of_games,
        }
        return prediction
    else:
        return "Invalid player ID(s): requested " + first_player + " and " + second_player
