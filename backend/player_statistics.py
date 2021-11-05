import copy
from google.cloud import datastore


def generate_player_statistics(start_timestamp, end_timestamp):
    client = datastore.Client()
    event_kind = 'Event_Data'
    query = client.query(kind=event_kind)
    query.add_filter('timestamp', '>=', start_timestamp)
    query.add_filter('timestamp', '<=', end_timestamp)
    game_list = list(query.fetch())
    generate_statistics(game_list)


def create_statistics_dict(statistics_struct, start_timestamp, end_timestamp):
    glicko_struct = dict()
    glicko_struct['rating_timestamp'] = 0
    glicko_struct['rating_deviation'] = 350
    glicko_struct['rating'] = 1000
    game_stats_struct = dict()
    game_stats_struct['total_games_played'] = 0
    game_stats_struct['total_games_won'] = 0
    game_stats_struct['total_player_points'] = 0
    game_stats_struct['total_opponent_points'] = 0
    game_stats_struct['sum_of_biggest_leads'] = 0
    game_stats_struct['sum_of_service_points_won'] = 0
    game_stats_struct['sum_of_service_points_lost'] = 0
    game_stats_struct['sum_of_receiver_points_won'] = 0
    game_stats_struct['sum_of_receiver_points_lost'] = 0
    game_stats_struct['sum_of_max_points_in_a_row'] = 0
    game_stats_struct['total_games_with_comeback_wins'] = 0
    game_stats_struct['sum_of_comeback_to_win'] = 0
    game_stats_struct['sum_of_service_errors'] = 0
    match_stats_struct = dict()
    match_stats_struct['total_matches'] = 0
    match_stats_struct['total_wins'] = 0
    match_stats_struct['overall'] = copy.deepcopy(game_stats_struct)
    match_stats_struct['game1'] = copy.deepcopy(game_stats_struct)
    match_stats_struct['game2'] = copy.deepcopy(game_stats_struct)
    match_stats_struct['game3'] = copy.deepcopy(game_stats_struct)
    match_stats_struct['game4'] = copy.deepcopy(game_stats_struct)
    match_stats_struct['game5'] = copy.deepcopy(game_stats_struct)
    statistics_struct['start_timestamp'] = start_timestamp
    statistics_struct['end_timestamp'] = end_timestamp
    statistics_struct['all_matches'] = copy.deepcopy(match_stats_struct)
    statistics_struct['stronger_opponents'] = copy.deepcopy(match_stats_struct)
    statistics_struct['weaker_opponents'] = copy.deepcopy(match_stats_struct)
    statistics_struct['matched_opponents'] = copy.deepcopy(match_stats_struct)
    statistics_struct['glicko_rating'] = glicko_struct


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
    for i in range(1,6):
        if 'period' + str(i) in event_data[player_score_name]:
            event_data_for_player['game' + str(i)] = dict()
            parse_individual_statistics(is_home, i, event_data, event_data_for_player['game' + str(i)])

    return event_data_for_player


def get_service_points(service_points: str):
    return_value = service_points.split("/")[0]
    return_value = int(return_value)
    return return_value


def parse_individual_statistics(is_home: bool, period: int, event_data: dict, player_event_data: dict):
    score_name = "homeScore"
    opponent_score_name = "awayScore"
    side = 'home'
    opp_side = 'away'
    if not is_home:
        score_name = "awayScore"
        opponent_score_name = "homeScore"
        side = 'away'
        opp_side = 'home'
    if period == 0:
        period_name = 'current'
        statistics_name = 'overall_statistics'
        player_event_data['games_won'] = int(event_data[score_name][period_name])
        player_event_data['games_played'] = player_event_data['games_won'] + \
                                            int(event_data[opponent_score_name][period_name])
    else:
        period_name = 'period' + str(period)
        statistics_name = 'statistics_' + period_name
        if period_name in event_data[score_name]:
            player_event_data['games_played'] = 1
            if event_data[score_name][period_name] > event_data[opponent_score_name][period_name]:
                player_event_data['games_won'] = 1
            else:
                player_event_data['games_won'] = 0

    if statistics_name in event_data:
        player_event_data['total_points'] = int(event_data[statistics_name]['Points won'][side])
        player_event_data['opponent_points'] = int(event_data[statistics_name]['Points won'][opp_side])
        player_event_data['biggest_lead'] = int(event_data[statistics_name]['Biggest lead'][side])
        player_event_data['service_points_won'] = \
            get_service_points(event_data[statistics_name]['Service points won'][side])
        player_event_data['service_points_lost'] = \
            get_service_points(event_data[statistics_name]['Receiver points won'][opp_side])
        player_event_data['receiver_points_won'] = \
            get_service_points(event_data[statistics_name]['Receiver points won'][side])
        player_event_data['receiver_points_lost'] = \
            get_service_points(event_data[statistics_name]['Service points won'][opp_side])
        player_event_data['service_errors'] = int(event_data[statistics_name]['Service errors'][side])
        player_event_data['max_points_in_a_row'] = int(event_data[statistics_name]['Max points in a row'][side])
        player_event_data['comeback_points'] = int(event_data[statistics_name]['Comeback to win'][side])


def generate_statistics(all_games: list):
    player_statistics = dict()
    statistics_struct = dict()

    start_timestamp = 2147483647
    end_timestamp = 0
    for game in all_games:
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

    print(player_statistics)


def add_raw_data(player: dict, game: dict):
    data_sets = ['overall', 'game1', 'game2', 'game3', 'game4', 'game5']
    player['total_matches'] += 1
    player['total_wins'] += game['match_win']
    for set_name in data_sets:
        if set_name in game:
            player[set_name]['total_games_played'] += game[set_name]['games_played']
            player[set_name]['total_games_won'] += game[set_name]['games_won']
            player[set_name]['total_player_points'] += game[set_name]['total_points']
            player[set_name]['total_opponent_points'] += game[set_name]['opponent_points']
            player[set_name]['sum_of_biggest_leads'] += game[set_name]['biggest_lead']
            player[set_name]['sum_of_service_points_won'] += game[set_name]['service_points_won']
            player[set_name]['sum_of_receiver_points_won'] += game[set_name]['receiver_points_won']
            player[set_name]['sum_of_service_points_lost'] += game[set_name]['service_points_lost']
            player[set_name]['sum_of_receiver_points_lost'] += game[set_name]['receiver_points_lost']
            player[set_name]['sum_of_max_points_in_a_row'] += game[set_name]['max_points_in_a_row']
            player[set_name]['sum_of_service_errors'] += game[set_name]['service_errors']
            if game[set_name]['comeback_points'] > 0:
                player[set_name]['total_games_with_comeback_wins'] += 1
                player[set_name]['sum_of_comeback_to_win'] += game[set_name]['comeback_points']

if __name__ == '__main__':
    generate_player_statistics(1586605800, 1586610600)