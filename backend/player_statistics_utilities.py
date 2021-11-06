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
    game_stats_struct['total_games_with_comeback_losses'] = 0
    game_stats_struct['sum_of_comeback_losses'] = 0
    game_stats_struct['sum_of_service_errors'] = 0
    game_stats_struct['win_rate'] = 0
    game_stats_struct['average_points'] = 0
    game_stats_struct['average_opponent_points'] = 0
    game_stats_struct['average_biggest_lead'] = 0
    game_stats_struct['average_service_points_won'] = 0
    game_stats_struct['average_service_points_lost'] = 0
    game_stats_struct['average_receiver_points_won'] = 0
    game_stats_struct['average_receiver_points_lost'] = 0
    game_stats_struct['average_max_points_in_a_row'] = 0
    game_stats_struct['average_comeback_to_win'] = 0
    game_stats_struct['average_comeback_loss'] = 0
    game_stats_struct['average_service_error'] = 0
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
        if 'Points won' in event_data[statistics_name]:
            player_event_data['total_points'] = int(event_data[statistics_name]['Points won'][side])
            player_event_data['opponent_points'] = int(event_data[statistics_name]['Points won'][opp_side])
        if 'Biggest lead' in event_data[statistics_name]:
            player_event_data['biggest_lead'] = int(event_data[statistics_name]['Biggest lead'][side])
        if 'Service points won' in event_data[statistics_name]:
            player_event_data['service_points_won'] = \
                get_service_points(event_data[statistics_name]['Service points won'][side])
            player_event_data['receiver_points_lost'] = \
                get_service_points(event_data[statistics_name]['Service points won'][opp_side])
        if 'Receiver points won' in event_data[statistics_name]:
            player_event_data['receiver_points_won'] = \
                get_service_points(event_data[statistics_name]['Receiver points won'][side])
            player_event_data['service_points_lost'] = \
                get_service_points(event_data[statistics_name]['Receiver points won'][opp_side])
        if 'Service errors' in event_data[statistics_name]:
            player_event_data['service_errors'] = int(event_data[statistics_name]['Service errors'][side])
        if 'Max points in a row' in event_data[statistics_name]:
            player_event_data['max_points_in_a_row'] = int(event_data[statistics_name]['Max points in a row'][side])
        if 'Comeback to win' in event_data[statistics_name]:
            player_event_data['comeback_points'] = int(event_data[statistics_name]['Comeback to win'][side])
            player_event_data['opponent_comeback_points'] = int(event_data[statistics_name]['Comeback to win'][opp_side])


def derive_statistics(statistics: dict):
    if 'total_games_played' in statistics and statistics['total_games_played'] > 0:
        num_games = statistics['total_games_played']
        if 'total_games_won' in statistics:
            statistics['win_rate'] = statistics['total_games_won'] / num_games
        if 'total_player_points' in statistics:
            statistics['average_points'] = statistics['total_player_points'] / num_games
        if 'total_opponent_points' in statistics:
            statistics['average_opponent_points'] = statistics['total_opponent_points'] / num_games
        if 'sum_of_biggest_leads' in statistics:
            statistics['average_biggest_lead'] = statistics['sum_of_biggest_leads'] / num_games
        if 'sum_of_service_points_won' in statistics:
            statistics['average_service_points_won'] = statistics['sum_of_service_points_won'] / num_games
        if 'sum_of_service_points_lost' in statistics:
            statistics['average_service_points_lost'] = statistics['sum_of_service_points_lost'] / num_games
        if 'sum_of_receiver_points_won' in statistics:
            statistics['average_receiver_points_won'] = statistics['sum_of_receiver_points_won'] / num_games
        if 'sum_of_receiver_points_lost' in statistics:
            statistics['average_receiver_points_lost'] = statistics['sum_of_receiver_points_lost'] / num_games
        if 'sum_of_max_points_in_a_row' in statistics:
            statistics['average_max_points_in_a_row'] = statistics['sum_of_max_points_in_a_row'] / num_games
        if statistics['total_games_with_comeback_wins'] > 0:
            statistics['average_comeback_to_win'] = statistics['sum_of_comeback_to_win'] / \
                                                    statistics['total_games_with_comeback_wins']
        if statistics['total_games_with_comeback_losses'] > 0:
            statistics['average_comeback_loss'] = statistics['sum_of_comeback_losses'] / \
                                                  statistics['total_games_with_comeback_losses']
        statistics['average_service_error'] = statistics['sum_of_service_errors'] / num_games


def add_raw_data(player: dict, game: dict):
    data_sets = ['overall', 'game1', 'game2', 'game3', 'game4', 'game5']
    player['total_matches'] += 1
    player['total_wins'] += game['match_win']
    for set_name in data_sets:
        if set_name in game:
            player[set_name]['total_games_played'] += game[set_name]['games_played']
            player[set_name]['total_games_won'] += game[set_name]['games_won']
            if 'total_points' in game[set_name]:
                player[set_name]['total_player_points'] += game[set_name]['total_points']
                if 'opponent_points' in game[set_name]:
                    player[set_name]['total_opponent_points'] += game[set_name]['opponent_points']
                if 'biggest_lead' in game[set_name]:
                    player[set_name]['sum_of_biggest_leads'] += game[set_name]['biggest_lead']
                if 'service_points_won' in game[set_name]:
                    player[set_name]['sum_of_service_points_won'] += game[set_name]['service_points_won']
                if 'receiver_points_won' in game[set_name]:
                    player[set_name]['sum_of_receiver_points_won'] += game[set_name]['receiver_points_won']
                if 'service_points_lost' in game[set_name]:
                    player[set_name]['sum_of_service_points_lost'] += game[set_name]['service_points_lost']
                if 'receiver_points_lost' in game[set_name]:
                    player[set_name]['sum_of_receiver_points_lost'] += game[set_name]['receiver_points_lost']
                if 'max_points_in_a_row' in game[set_name]:
                    player[set_name]['sum_of_max_points_in_a_row'] += game[set_name]['max_points_in_a_row']
                if 'service_errors' in game[set_name]:
                    player[set_name]['sum_of_service_errors'] += game[set_name]['service_errors']
                if 'comeback_points' in game[set_name] and game[set_name]['comeback_points'] > 0:
                    player[set_name]['total_games_with_comeback_wins'] += 1
                    player[set_name]['sum_of_comeback_to_win'] += game[set_name]['comeback_points']
                if 'opponent_comeback_points' in game[set_name] and game[set_name]['opponent_comeback_points'] > 0:
                    player[set_name]['total_games_with_comeback_losses'] += 1
                    player[set_name]['sum_of_comeback_losses'] += game[set_name]['opponent_comeback_points']
            else:
                print('partial data set for ' + set_name)


def update_glicko_rating(p1_rating: dict, p2_rating: dict, timestamp: int, p1_win: bool):
