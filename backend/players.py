from google.cloud import datastore


def get_all_players():
    # Instantiates a client
    datastore_client = datastore.Client()

    players = list()

    query = datastore_client.query(kind='Player')
    query_iter = query.fetch()
    for entity in query_iter:
        name = entity['name']
        key = entity.key.id
        players.append({"name": name, "id": key})

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
