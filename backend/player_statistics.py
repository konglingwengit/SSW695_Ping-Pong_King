import copy
from google.cloud import datastore
from player_statistics_utilities import create_statistics_dict, parse_individual_statistics
from player_statistics_utilities import derive_statistics, add_raw_data
from player_statistics_utilities import update_glicko_rating


def generate_player_statistics(start_timestamp, end_timestamp):
    print('Creating client to read')
    client = datastore.Client()
    event_kind = 'Event_Data'
    query = client.query(kind=event_kind)
    query.add_filter('timestamp', '>=', start_timestamp)
    query.add_filter('timestamp', '<=', end_timestamp)
    query.order('timestamp')
    print('Fetching data')
    game_list = list(query.fetch())
    generate_statistics(game_list)


def build_player_game_data(player_id, event_data):
    is_home = True
    event_data_for_player = dict()
    event_data_for_player['overall'] = dict()
    player_score_name = 'homeScore'
    if event_data['awayTeam'] == player_id:
        player_score_name = 'awayScore'
        is_home = False
    if event_data[player_score_name]['current'] == 3:
        event_data_for_player['match_win'] = 1
    else:
        event_data_for_player['match_win'] = 0
    event_data_for_player['timestamp'] = event_data['timestamp']

    parse_individual_statistics(is_home, 0, event_data, event_data_for_player['overall'])
    for i in range(1, 6):
        if 'period' + str(i) in event_data[player_score_name]:
            event_data_for_player['game' + str(i)] = dict()
            parse_individual_statistics(is_home, i, event_data, event_data_for_player['game' + str(i)])

    return event_data_for_player


def generate_statistics(all_games: list):
    player_statistics = dict()
    statistics_struct = dict()

    start_timestamp = 2147483647
    end_timestamp = 0
    game_number = 1
    for game in all_games:

        # Progress reporting - processing
        print('game ' + str(game_number) + ' of ' + str(len(all_games)))
        game_number += 1

        if int(game['timestamp']) > end_timestamp:
            end_timestamp = int(game['timestamp'])
        if int(game['timestamp']) < start_timestamp:
            start_timestamp = int(game['timestamp'])

    create_statistics_dict(statistics_struct, start_timestamp, end_timestamp)

    for game in all_games:
        if game['homeTeam'] not in player_statistics:
            player_statistics[game['homeTeam']] = copy.deepcopy(statistics_struct)
        if game['awayTeam'] not in player_statistics:
            player_statistics[game['awayTeam']] = copy.deepcopy(statistics_struct)

    for player in player_statistics:
        for game in all_games:
            if game['homeTeam'] == player or game['awayTeam'] == player:

                # Update Glicko rating here

                player_game_data = build_player_game_data(player, game)
                add_raw_data(player_statistics[player]['all_matches'], player_game_data)

                # Add weaker, stronger, similar, and individual opponents

    for player in player_statistics:
        derive_statistics(player_statistics[player]['all_matches']['overall'])
        derive_statistics(player_statistics[player]['all_matches']['game1'])
        derive_statistics(player_statistics[player]['all_matches']['game2'])
        derive_statistics(player_statistics[player]['all_matches']['game3'])
        derive_statistics(player_statistics[player]['all_matches']['game4'])
        derive_statistics(player_statistics[player]['all_matches']['game5'])
        # Add weaker, stronger, similar, and individual opponents

    add_to_db(player_statistics)


def add_to_db(player_statistics):
    print('Creating client to write')
    client = datastore.Client()

    statistic_kind = 'Player_Statistic_Data'

    player_number = 1
    for player in player_statistics:

        # Progress logging
        print('Writing player ' + str(player_number) + ' of ' + str(len(player_statistics)))
        player_number += 1

        entity = datastore.entity.Entity()
        entity.key = client.key(statistic_kind, int(player))
        for element in player_statistics[player]:
            entity[element] = player_statistics[player][element]
        # client.put(entity)


if __name__ == '__main__':
    # generate_player_statistics(1586605800, 1635611400)
    generate_player_statistics(1586605800, 1590000000)
