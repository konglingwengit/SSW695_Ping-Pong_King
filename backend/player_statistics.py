import random
from google.cloud import datastore


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
