import copy
import random
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

        if not (game['winnerCode'] == 1 or game['winnerCode'] == 2):
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
    output_list = []
    try:
        statistic_data = client.get(client.key('Player_Statistic_Data', int(player_id)))
        output_list.append([{'name': 'Rating', 'data': round(statistic_data['glicko_rating']['rating'], 0)},
                            {'name': 'Total Matches Played', 'data': statistic_data['all_matches']['total_matches']},
                            {'name': 'Total Matches Won', 'data': statistic_data['all_matches']['total_wins']}])
        for i in range(0, 6):
            add_random_stat(output_list[0], statistic_data)
    except:
        output_list.append([{'name': 'Failed to retrieve statistics', 'data': ''}])
    return output_list


def get_vs_stats(player_1_id, player_2_id):
    client = datastore.Client()
    output_list = []
    try:
        p1_statistic_data = client.get(client.key('Player_Statistic_Data', int(player_1_id)))
        p2_statistic_data = client.get(client.key('Player_Statistic_Data', int(player_2_id)))

        if str(player_2_id) in p1_statistic_data['specific_opponent']:
            p1_data = p1_statistic_data['specific_opponent'][str(player_2_id)]['overall']
            p2_data = p2_statistic_data['specific_opponent'][str(player_1_id)]['overall']
            matches = p1_statistic_data['specific_opponent'][str(player_2_id)]['total_matches']
            first_wins = p1_statistic_data['specific_opponent'][str(player_2_id)]['total_wins']
            second_wins = p2_statistic_data['specific_opponent'][str(player_1_id)]['total_wins']
            output_list.append({'name': 'Rating',
                                'data_p1': round(p1_statistic_data['glicko_rating']['rating']),
                                'data_p2': round(p2_statistic_data['glicko_rating']['rating'])})
            output_list.append({'name': 'Total Matches',
                                'data_p1': matches,
                                'data_p2': matches})
            output_list.append({'name': 'Total Matches Won',
                                'data_p1': first_wins,
                                'data_p2': second_wins})
            output_list.append({'name': 'Total Games Won',
                                'data_p1': p1_data['total_games_won'],
                                'data_p2': p2_data['total_games_won']})
            output_list.append({'name': 'Total Games Lost',
                                'data_p1': p1_data['total_games_played'] - p1_data['total_games_won'],
                                'data_p2': p2_data['total_games_played'] - p2_data['total_games_won']})
            output_list.append({'name': 'Total Points Scored',
                                'data_p1': p1_data['total_player_points'],
                                'data_p2': p2_data['total_player_points']})
            output_list.append({'name': 'Service Points Scored',
                                'data_p1': p1_data['sum_of_service_points_won'],
                                'data_p2': p2_data['sum_of_service_points_won']})
            output_list.append({'name': 'Receiving Points Scored',
                                'data_p1': p1_data['sum_of_receiver_points_won'],
                                'data_p2': p2_data['sum_of_receiver_points_won']})
            output_list.append({'name': 'Average max points in a row',
                                'data_p1': round(p1_data['sum_of_max_points_in_a_row']/matches, 1),
                                'data_p2': round(p2_data['sum_of_max_points_in_a_row']/matches, 1)})
            output_list.append({'name': 'Average biggest lead',
                                'data_p1': round(p1_data['sum_of_biggest_leads']/matches, 1),
                                'data_p2': round(p2_data['sum_of_biggest_leads']/matches, 1)})
    except:
        print(f'Failed to retrieve data for {player_1_id} and {player_2_id}.')

    # If we retrieved data, but there were no matches, provide an empty set.
    if len(output_list) == 0:
        output_list.append({'name': '', 'data_p1': '', 'data_p2': ''})

    return output_list


def add_random_stat(output: list, statistics: dict):
    list_of_categories = ['all_matches', 'stronger_opponents', 'weaker_opponents', 'matched_opponents']
    list_of_category_strings = ['in all matches', 'against stronger opponents',
                                'against weaker opponents', 'in evenly matched games']
    list_of_games = ['overall', 'game1', 'game2', 'game3', 'game4', 'game5']
    list_of_game_strings = ['in all games', 'in game 1', 'in game 2', 'in game 3', 'in game 4', 'in game 5']
    list_of_statistics = ['total_games_played', 'total_games_won', 'total_player_points', 'total_opponent_points',
                          'total_games_with_comeback_wins', 'sum_of_service_errors', 'win_rate',
                          'average_points', 'average_opponent_points', 'average_biggest_lead',
                          'average_service_points_won', 'average_service_points_lost', 'average_receiver_points_won',
                          'average_receiver_points_lost', 'average_max_points_in_a_row', 'average_comeback_to_win',
                          'average_comeback_loss', 'average_service_error']
    data = 0
    # Statistics of 0 typically mean we have no data for that particular item, so don't send them out.
    while data == 0:
        category_index = random.randrange(0, len(list_of_categories))
        game_index = random.randrange(0, len(list_of_games))
        statistic = random.randrange(0, len(list_of_statistics))
        name = list_of_statistics[statistic].capitalize().replace('_', ' ') + ' ' + \
            list_of_category_strings[category_index] + ' ' + list_of_game_strings[game_index]
        data = statistics[list_of_categories[category_index]][list_of_games[game_index]][list_of_statistics[statistic]]

    output.append({'name': name, 'data': round(data, 2)})
