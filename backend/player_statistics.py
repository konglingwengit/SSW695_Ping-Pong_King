import copy
from google.cloud import datastore
from player_statistics_utilities import create_statistics_dict, parse_individual_statistics
from player_statistics_utilities import derive_statistics, add_raw_data, add_opponent_data
from player_statistics_utilities import update_glicko_rating


def generate_player_statistics(start_timestamp, end_timestamp):
    print('Creating client to read')
    client = datastore.Client()
    event_kind = 'Event_Data'
    query = client.query(kind=event_kind)
    query.add_filter('timestamp', '>=', start_timestamp)
    query.add_filter('timestamp', '<=', end_timestamp)
    query.order = ['timestamp']
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

    # Build up the dictionary for all the players we're processing
    for game in all_games:
        if game['winnerCode'] == 1 or game['winnerCode'] == 2:
            if game['homeTeam'] not in player_statistics:
                player_statistics[game['homeTeam']] = copy.deepcopy(statistics_struct)
            if game['awayTeam'] not in player_statistics:
                player_statistics[game['awayTeam']] = copy.deepcopy(statistics_struct)

    # Actually run the processing
    for game in all_games:

        if not(game['winnerCode'] == 1 or game['winnerCode'] == 2):
            continue

        player_list = [game['homeTeam'], game['awayTeam']]
        winner_index = game['winnerCode'] - 1
        loser_index = 1 - (game['winnerCode'] - 1)

        # Update Glicko rating
        winner_rating = player_statistics[player_list[winner_index]]['glicko_rating']
        loser_rating = player_statistics[player_list[loser_index]]['glicko_rating']
        update_glicko_rating(winner_rating, loser_rating, game['timestamp'])

        # Update game statistics
        acceptable_deviation = 100
        similar_strength = 100
        for player in player_list:
            if player == player_list[0]:
                other_player = player_list[1]
            else:
                other_player = player_list[0]
            player_game_data = build_player_game_data(player, game)
            add_raw_data(player_statistics[player]['all_matches'], player_game_data)

            player_deviation = player_statistics[player]['glicko_rating']['rating_deviation']
            player_rating = player_statistics[player]['glicko_rating']['rating']
            other_deviation = player_statistics[other_player]['glicko_rating']['rating_deviation']
            other_rating = player_statistics[other_player]['glicko_rating']['rating']
            if player_deviation < acceptable_deviation and other_deviation < acceptable_deviation:
                if player_rating - other_rating > similar_strength:
                    add_raw_data(player_statistics[player]['weaker_opponents'], player_game_data)
                elif other_rating - player_rating > similar_strength:
                    add_raw_data(player_statistics[player]['stronger_opponents'], player_game_data)
                else:
                    add_raw_data(player_statistics[player]['matched_opponents'], player_game_data)

            add_opponent_data(player_statistics[player], other_player, player_game_data)

    categories = ['all_matches', 'weaker_opponents', 'stronger_opponents', 'matched_opponents']
    game_categories = ['overall', 'game1', 'game2', 'game3', 'game4', 'game5']
    for player in player_statistics:
        for category in categories:
            for game_category in game_categories:
                if category in player_statistics[player] and game_category in player_statistics[player][category]:
                    derive_statistics(player_statistics[player][category][game_category])
        for opponent in player_statistics[player]['specific_opponent']:
            for game_category in game_categories:
                if game_category in player_statistics[player]['specific_opponent'][opponent]:
                    derive_statistics(player_statistics[player]['specific_opponent'][opponent][game_category])

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
        client.put(entity)


def get_player_stats(player_id):
    client = datastore.Client()
    statistic_data = client.get(client.key('Player_Statistic_Data', int(player_id)))
    return statistic_data


def get_vs_stats(player_1_id, player_2_id):
    client = datastore.Client()
    p1_statistic_data = client.get(client.key('Player_Statistic_Data', int(player_1_id)))
    p2_statistic_data = client.get(client.key('Player_Statistic_Data', int(player_2_id)))
    output_list = list([None, None, None, None, None, None])
    output_list[0] = ['Rating', 'Total Matches Played', 'Total Matches Won']
    output_list[1] = [p1_statistic_data['glicko_rating']['rating'], p1_statistic_data['all_matches']['total_matches'],
                      p1_statistic_data['all_matches']['total_wins']]
    output_list[2] = ['Versus Matches Played', 'First Player Matches Won', 'Second Player Matches Won']
    if str(player_2_id) in p1_statistic_data['specific_opponent']:
        output_list[3] = [p1_statistic_data['specific_opponent'][str(player_2_id)]['total_matches'],
                          p1_statistic_data['specific_opponent'][str(player_2_id)]['total_wins'],
                          p2_statistic_data['specific_opponent'][str(player_1_id)]['total_wins']]
    else:
        output_list[3] = [0, 0, 0]
    output_list[4] = ['Rating', 'Total Matches Played', 'Total Matches Won']
    output_list[5] = [p2_statistic_data['glicko_rating']['rating'], p2_statistic_data['all_matches']['total_matches'],
                      p2_statistic_data['all_matches']['total_wins']]

    return output_list
