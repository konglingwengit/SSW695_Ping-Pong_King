from typing import Dict

input_players: Dict = dict()


def get_all_players():
    global input_players
    if len(input_players) == 0:
        # Normal path
        players = list()
        players.append({"id": "1", "name": "Lingwen Kong"})
        players.append({"id": "2", "name": "Deepti Argawal"})
        players.append({"id": "3", "name": "Dekun Chen"})
        players.append({"id": "4", "name": "Bin Sun"})
        players.append({"id": "5", "name": "Jonathan Sebast"})
    else:
        # Used for unit testing
        players = input_players

    return players


def player_exists(player_id: str):
    players = get_all_players()
    for player in players:
        if player['id'] == player_id:
            return True
    return False


def get_player_name(player_id: str):
    players = get_all_players()
    for player in players:
        if player['id'] == player_id:
            return player['name']
    return None


# Support for unit testing
def set_player_list(test_list):
    global input_players
    input_players = test_list
