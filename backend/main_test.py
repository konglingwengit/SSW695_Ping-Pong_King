import main
from google.cloud import datastore
from players import get_player_name

datastore_client = datastore.Client()


def test_get_players():
    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/api/players')
    returned_data = r.get_json()

    query = datastore_client.query(kind='Player')
    db_players = list(query.fetch())

    assert len(returned_data) == len(db_players)
    assert 'name' in returned_data[0]


def test_main_predictions():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/api/predictions')
    assert 'Not yet implemented' in r.data.decode('utf-8')

    r = client.get('/api/predictions?prediction=WINNER&p1=345227&p2=347571')
    returned_data = r.get_json()
    assert returned_data['title'] == 'Winning Player'
    assert returned_data['line1'] == get_player_name("345227") or returned_data['line1'] == get_player_name("347571")

    r = client.get('/api/predictions?prediction=WINNER&p1=99&p2=347571')
    returned_data = r.get_json()
    assert returned_data['title'] == 'Winning Player'
    assert 'Prediction Failed' in returned_data['line1']

    r = client.get('/api/predictions?prediction=FIRST_GAME&p1=345227&p2=345240')
    returned_data = r.get_json()
    assert returned_data['title'] == 'First Game Winner'
    assert returned_data['line1'] == get_player_name("345227") or returned_data['line1'] == get_player_name("345240")

    r = client.get('/api/predictions?prediction=FIRST_GAME&p1=1&p2=2')
    returned_data = r.get_json()
    assert 'Prediction Failed' in returned_data['line1']

    r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=345227&p2=345240')
    returned_data = r.get_json()
    assert returned_data['title'] == 'Number of Games'
    assert 3 <= int(returned_data['line1']) <= 5

    r = client.get('/api/predictions?prediction=NUMBER_OF_GAMES&p1=1&p2=2')
    returned_data = r.get_json()
    assert 'Prediction Failed' in returned_data['line1']

    r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=345227&p2=345240')
    returned_data = r.get_json()
    assert returned_data['title'] == 'Total Points'
    assert 'Fewer' in returned_data['line1'] or 'More' in returned_data['line1']
    assert '79' in returned_data['line1']

    r = client.get('/api/predictions?prediction=TOTAL_POINTS&p1=1&p2=2')
    returned_data = r.get_json()
    assert 'Prediction Failed' in returned_data['line1']

    r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=345227&p2=345240')
    returned_data = r.get_json()
    assert returned_data['title'] == 'Games Decided By Extra Points'
    assert 0 <= int(returned_data['line1']) <= 5

    r = client.get('/api/predictions?prediction=EXTRA_POINTS&p1=1&p2=2')
    returned_data = r.get_json()
    assert 'Prediction Failed' in returned_data['line1']

    r = client.get('/api/predictions?prediction=ALL&p1=345227&p2=345240')
    returned_data = r.get_json()
    assert len(returned_data) == 5
    assert returned_data[0]['title'] == 'Winning Player'
    assert returned_data[1]['title'] == 'Total Points'
    assert returned_data[2]['title'] == 'Number of Games'
    assert returned_data[3]['title'] == 'First Game Winner'
    assert returned_data[4]['title'] == 'Games Decided By Extra Points'

    # Swap the two players, so we get both P1 and P2 winning in relevant tests
    r = client.get('/api/predictions?prediction=ALL&p1=345240&p2=345227')
    returned_data = r.get_json()
    assert len(returned_data) == 5
    assert returned_data[0]['title'] == 'Winning Player'
    assert returned_data[1]['title'] == 'Total Points'
    assert returned_data[2]['title'] == 'Number of Games'
    assert returned_data[3]['title'] == 'First Game Winner'
    assert returned_data[4]['title'] == 'Games Decided By Extra Points'

    r = client.get('/api/predictions?prediction=ALL&p1=1&p2=2')
    returned_data = r.get_json()
    assert 'Prediction Failed' in returned_data[0]['line1']


def test_main_statistics():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/api/single_player_stats?p1=1')
    returned_data = r.get_json()
    assert 'Failed' in returned_data[0][0]['name']

    r = client.get('/api/single_player_stats')
    returned_data = r.get_json()
    assert 'Not a valid player' in returned_data

    r = client.get('/api/single_player_stats?p1=345227')
    returned_data = r.get_json()
    for i in range(0, 9):
        assert len(returned_data[0][i]['name']) > 0
        assert returned_data[0][i]['data'] > 0

    r = client.get('/api/vs_stats')
    returned_data = r.get_json()
    assert 'Not a valid player' in returned_data

    r = client.get('/api/vs_stats?p1=345240')
    returned_data = r.get_json()
    assert 'Not a valid player' in returned_data

    r = client.get('/api/vs_stats?p2=347571')
    returned_data = r.get_json()
    assert 'Not a valid player' in returned_data

    r = client.get('/api/vs_stats?p1=1&p2=2')
    returned_data = r.get_json()
    assert returned_data[0]['name'] == ''

    r = client.get('/api/vs_stats?p1=345240&p2=347571')
    returned_data = r.get_json()
    for i in range(0, 10):
        assert len(returned_data[i]['name']) > 0
        # Some stats may be zero, where an opponent got no wins, for example.
        assert 'data_p1' in returned_data[i]
        assert 'data_p2' in returned_data[i]

    r = client.get('/api/vs_stats?p1=345227&p2=347571')
    returned_data = r.get_json()
    for i in range(0, 10):
        assert len(returned_data[i]['name']) > 0
        # Some stats may be zero, where an opponent got no wins, for example.
        assert 'data_p1' in returned_data[i]
        assert 'data_p2' in returned_data[i]

    r = client.get('/api/vs_stats?p1=345227&p2=292113')
    returned_data = r.get_json()
    assert returned_data[0]['name'] == ''


def test_main_users():
    main.app.testing = True
    client = main.app.test_client()

    r = client.post('/api/user/')
    returned_data = r.get_json()
    assert 'not authorized' in returned_data

    r = client.post('/api/user/', json={'email': 'fake@gmail.com'})
    returned_data = r.get_json()
    assert 'not authorized' in returned_data

    r = client.post('/api/user/', json={'email': 'test@gmail.com'})
    returned_data = r.get_json()
    assert 'User authorized' in returned_data
    assert 'test@gmail.com' in returned_data
