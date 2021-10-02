from typing import Dict


def get_all_players():
    players: Dict[Player] = {
        "1": "Lingwen Kong",
        "2": "Deepti Argawal",
        "3": "Dekun Chen",
        "4": "Bin Sun",
        "5": "Jonathan Sebast"
    }
    return players


def player_exists(player_id: str):
    players = get_all_players()
    if player_id in players:
        return True
    else:
        return False


def get_player_name(player_id: str):
    players = get_all_players()
    return players[player_id]
