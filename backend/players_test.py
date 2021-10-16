import players

my_list = [{"id": "1", "name": "Person's Name"},
           {"id": "2", "name": "Another Name"},
           {"id": "3", "name": "Pickled Herring"}]


def test_get_all_players():
    global my_list

    default_list = players.get_all_players()

    item_count = 0

    # Just making sure it returns a dictionary, since the
    #   definition of valid players will change.
    for key in default_list:
        item_count = item_count + 1

    assert item_count > 0

    players.set_player_list(my_list)

    new_list = players.get_all_players()

    for player in new_list:
        found = False
        for my_player in my_list:
            if player["name"] == my_player["name"] and player["id"] == my_player["id"]:
                found = True
        assert found

    assert len(my_list) == len(new_list)


def test_player_exists():
    global my_list
    players.set_player_list(my_list)

    assert players.player_exists("1")
    assert not players.player_exists("Buffalo")
    assert not players.player_exists("7")
    assert players.player_exists("3")


def test_get_player_name():
    global my_list
    players.set_player_list(my_list)

    assert players.get_player_name("1") == "Person's Name"
    assert players.get_player_name("3") == "Pickled Herring"
    assert players.get_player_name("X") is None
