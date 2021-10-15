import main
import players


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Hello World' in r.data.decode('utf-8')


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
    my_players = {"1": "George", "99": "Samuel", "300": "Susan"}
    players.set_player_list(my_players)

    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/api/predictions')
    assert 'Not yet implemented' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=WINNER&p1=99&p2=300')
    returned_data = r.get_json()
    assert 0 < float(returned_data['Win Chance']) <= 1
    assert returned_data['Winner'] == "Samuel" or returned_data['Winner'] == "Susan"

    r = client.get('/api/predictions?prediction=WINNER&p1=99&p2=2')
    assert 'Invalid' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=THIRD_GAME&p1=1&p2=99')
    returned_data = r.get_json()
    assert returned_data['Third Game Winner'] == "Samuel" or returned_data['Third Game Winner'] == "George"

    r = client.get('/api/predictions?prediction=THIRD_GAME&p1=1&p2=2')
    assert 'Invalid' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=1&p2=99')
    returned_data = r.get_json()
    assert 3 <= int(returned_data['Number Of Games']) <= 5

    r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=1&p2=2')
    assert 'Invalid' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=1&p2=99')
    returned_data = r.get_json()
    assert int(returned_data['Total Points']) >= 33

    r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=1&p2=2')
    assert 'Invalid' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=1&p2=99')
    returned_data = r.get_json()
    assert 0 <= int(returned_data['Games Decided By Extra Points']) <= 5

    r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=1&p2=2')
    assert 'Invalid' in r.data.decode('utf-8')

