from typing import Dict

input_players: Dict = dict()


def get_all_players():
    global input_players
    if len(input_players) == 0:
        # Normal path
        players: Dict = {
            "1": "Lingwen Kong",
            "2": "Deepti Argawal",
            "3": "Dekun Chen",
            "4": "Bin Sun",
            "5": "Jonathan Sebast"
        }
    else:
        # Used for unit testing
        players = input_players

    return players


def player_exists(player_id: str):
    players = get_all_players()
    if player_id in players:
        return True
    else:
        return False


def get_player_name(player_id: str):
    players = get_all_players()
    if player_id in players:
        return players[player_id]
    else:
        return None


# Support for unit testing
def set_player_list(test_list: Dict):
    global input_players
    input_players = test_list
