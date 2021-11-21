import players

from google.cloud import datastore

datastore_client = datastore.Client()


def test_get_all_players():
    default_list = players.get_all_players()

    item_count = 0

    # Just making sure it returns a dictionary, since the
    #   definition of valid players will change.
    for key in default_list:
        item_count = item_count + 1

    assert item_count > 0

    new_list = players.get_all_players()

    query = datastore_client.query(kind='Player')
    db_players = list(query.fetch())

    for player in new_list:
        found = False
        for my_player in db_players:
            if player["name"] == my_player["name"] and player["id"] == my_player.id:
                found = True
        assert found

    assert len(db_players) == len(new_list)


def test_player_exists():
    assert players.player_exists("345227")
    assert not players.player_exists("Buffalo")
    assert not players.player_exists("7")
    assert players.player_exists("347571")


def test_get_player_name():
    assert players.get_player_name("1") == "Unknown Player"
    assert players.get_player_name("345227") == "Vavrenyuk S."
    assert players.get_player_name("347571") == "Nechitaylo E."
    assert players.get_player_name("345240") == "Khorolsky V."
    assert players.get_player_name("X") == "Unknown Player"
