from typing import Dict
from google.cloud import datastore

input_players: Dict = dict()


def get_all_players():
    global input_players
    if len(input_players) == 0:
        # Normal path

        # Instantiates a client
        datastore_client = datastore.Client()

        players = list()

        query = datastore_client.query(kind='Player')
        query_iter = query.fetch()
        for entity in query_iter:
            name = entity['name']
            key = entity.key.id
            players.append({"name": name, "id": key})

    else:
        # Used for unit testing
        players = input_players

    return players


def player_exists(player_id: str):
    if player_id.isdigit():
        players = get_all_players()
        for player in players:
            if int(player['id']) == int(player_id):
                return True
    return False


def get_player_name(player_id: str):
    if player_id.isdigit():
        players = get_all_players()
        for player in players:
            if int(player['id']) == int(player_id):
                return player['name']
    return "Unknown Player"


# Support for unit testing
def set_player_list(test_list):
    global input_players
    input_players = test_list
