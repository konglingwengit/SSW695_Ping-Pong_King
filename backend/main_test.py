import main
import players


def test_get_players():
    my_players = {"1": "George", "X": "Samuel"}
    players.set_player_list(my_players)

    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/api/players')

    returned_data = r.get_json()
    assert len(returned_data) == len(my_players)
    for key in returned_data:
        assert my_players[key] == returned_data[key]


def test_main_predictions():
    my_players = [{"id": "1", "name": "George"}, {"id": "99", "name": "Samuel"}, {"id": "300", "name": "Susan"}]
    players.set_player_list(my_players)

    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/api/predictions')
    assert 'Not yet implemented' in r.data.decode('utf-8')

    # r = client.get('/api/predictions?prediction=WINNER&p1=99&p2=300')
    # returned_data = r.get_json()
    # assert 0 < float(returned_data['win_chance']) <= 1
    # assert returned_data['winner_name'] == "Samuel" or returned_data['winner_name'] == "Susan"
    # assert returned_data['winner_id'] == "99" or returned_data['winner_id'] == "300"

    # r = client.get('/api/predictions?prediction=WINNER&p1=99&p2=2')
    # assert 'Invalid' in r.data.decode('utf-8')

    # r = client.get('/api/predictions?prediction=THIRD_GAME&p1=1&p2=99')
    # returned_data = r.get_json()
    # assert returned_data['line1'] == "Samuel" or returned_data['line1'] == "George"
    #
    # r = client.get('/api/predictions?prediction=THIRD_GAME&p1=1&p2=2')
    # assert 'Invalid' in r.data.decode('utf-8')
    #
    # r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=1&p2=99')
    # returned_data = r.get_json()
    # assert 3 <= int(returned_data['line1']) <= 5
    #
    # r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=1&p2=2')
    # assert 'Invalid' in r.data.decode('utf-8')
    #
    # r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=1&p2=99')
    # returned_data = r.get_json()
    # assert int(returned_data['line1']) >= 33
    #
    # r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=1&p2=2')
    # assert 'Invalid' in r.data.decode('utf-8')
    #
    # r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=1&p2=99')
    # returned_data = r.get_json()
    # assert 0 <= int(returned_data['line1']) <= 5
    #
    # r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=1&p2=2')
    # assert 'Invalid' in r.data.decode('utf-8')
