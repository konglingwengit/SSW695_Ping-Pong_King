import players
import pytest

from flaskr import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_get_all_players:

    default_list = player.get_all_players()

    item_count = 0

    # Just making sure it returns a dictionary, since the
    #   definition of valid players will change.
    for key in default_list:
        item_count = item_count + 1

    assert item_count > 0

    my_list = {"Z" : "Person's Name",
              "X" : "A letter"
              }
    player.set_player_list(my_list)

    new_list = player.get_all_players()

    for key in new_list:
        assert new_list[key] = my_list[key]

    assert my_list.len() == new_list.len()
    