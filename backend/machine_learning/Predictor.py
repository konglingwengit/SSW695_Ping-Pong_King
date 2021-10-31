import json
from google.cloud import datastore

event_key = 'Event_Data'
client = None


def get_player_games(player_id: int):
    global client
    query = client.query(kind=event_key)
    query.add_filter('homeTeam', '=', player_id)
    player_a_home = list(query.fetch())
    query = client.query(kind=event_key)
    query.add_filter('awayTeam', '=', player_id)
    player_a_away = list(query.fetch())
    return player_a_home + player_a_away


def get_versus_games(a_id: int, b_id: int):
    global client
    query = client.query(kind=event_key)
    query.add_filter('homeTeam', '=', a_id)
    query.add_filter('awayTeam', '=', b_id)
    player_a_home = list(query.fetch())
    query = client.query(kind=event_key)
    query.add_filter('homeTeam', '=', b_id)
    query.add_filter('awayTeam', '=', a_id)
    player_b_home = list(query.fetch())
    return player_a_home + player_b_home


def combine_lists(list_a: list, list_b: list):
    combined = list_a
    for element_b in list_b:
        found = False
        for element_a in list_a:
            if element_a.key.id_or_name == element_b.key.id_or_name:
                found = True
                break
        if not found:
            combined.append(element_b)
    return combined


def predict_winner(a_id: int, b_id: int):
    global client
    if client is None:
        client = datastore.Client()
    result = dict()

    versus_games = get_versus_games(a_id, b_id)

    if len(versus_games) > 0:
        A_played = len(versus_games)
        A_won = 0
        B_played = len(versus_games)
        B_won = 0
        for i in versus_games:
            if i['winnerCode'] == 1:
                if a_id == i['homeTeam']:
                    A_won = A_won + 1
                else:
                    B_won = B_won + 1
            else:
                if a_id == i['awayTeam']:
                    A_won = A_won + 1
                else:
                    B_won = B_won + 1

        A_win_rate = (A_won / A_played) * 100
        B_win_rate = (B_won / B_played) * 100

        probability_A = (A_win_rate / (A_win_rate + B_win_rate)) * 100
        probability_B = (B_win_rate / (A_win_rate + B_win_rate)) * 100

        if B_win_rate > A_win_rate:
            result['winner_id'] = b_id
            result['win_chance'] = probability_B
        else:
            result['winner_id'] = a_id
            result['win_chance'] = probability_A

    else:

        player_a_games = get_player_games(a_id)
        player_b_games = get_player_games(b_id)

        if len(player_a_games) == 0 and len(player_b_games) == 0:
            print("No games were recorded for either player, so no conclusions can be drawn")
        else:
            A_won = 0
            B_won = 0
            for i in player_a_games:
                if i['winnerCode'] == 1:
                    if a_id == i['homeTeam']:
                        A_won = A_won + 1
                else:
                    if a_id == i['awayTeam']:
                        A_won = A_won + 1

            for i in player_b_games:
                if i['winnerCode'] == 1:
                    if b_id == i['homeTeam']:
                        B_won = B_won + 1
                else:
                    if b_id == i['awayTeam']:
                        B_won = B_won + 1

            if len(player_a_games) == 0:
                B_win_rate = B_won / len(player_b_games) * 100
                if B_win_rate > 50:
                    result['winner_id'] = b_id
                    result['win_chance'] = B_win_rate
                    result['confidence'] = "very low"
                else:
                    result['winner_id'] = a_id
                    result['win_chance'] = 100 - B_win_rate
                    result['confidence'] = "very low"
            elif len(player_b_games) == 0:
                A_win_rate = A_won / len(player_a_games) * 100
                if A_win_rate > 50:
                    result['winner_id'] = a_id
                    result['win_chance'] = A_win_rate
                    result['confidence'] = "very low"
                else:
                    result['winner_id'] = b_id
                    result['win_chance'] = 100 - A_win_rate
                    result['confidence'] = "very low"
            else:
                A_win_rate = A_won / len(player_a_games) * 100
                B_win_rate = B_won / len(player_b_games) * 100

                probability_A = (A_win_rate / (A_win_rate + B_win_rate)) * 100
                probability_B = (B_win_rate / (A_win_rate + B_win_rate)) * 100

                if probability_A > probability_B:
                    result['winner_id'] = a_id
                    result['win_chance'] = probability_A
                    result['confidence'] = "low"
                else:
                    result['winner_id'] = b_id
                    result['win_chance'] = probability_B
                    result['confidence'] = "low"
    print(result)
    return result
