import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from google.cloud import datastore
import pickle
from predictions_final import initialize_columns

df_game = None
df_player = None
player_column_names = None
game_column_names = None


def generate_models():
    global player_column_names
    global game_column_names
    player_column_names, game_column_names = initialize_columns()
    initialize_data_frames()
    initialize_who_win()
    initialize_exact_number()
    initialize_first_winner()
    initialize_extra_point()
    initialize_total_points()


def initialize_data_frames():
    # init. df
    global df_game
    global df_player

    print('Activating datastore')
    client = datastore.Client()

    query = client.query(kind='Player_Model_Data')
    print('Fetching player data')
    player_data = list(query.fetch())
    print('Player data fetched')

    data_array = np.zeros([len(player_column_names), len(player_data)])
    for idx, player in enumerate(player_data):
        for col in range(0, len(player_column_names)):
            data_array[col, idx] = player[player_column_names[col]]
    rows = len(player_data)
    player_data = None
    df_player = pd.DataFrame(data_array.transpose(), index=range(0, rows), columns=player_column_names)
    data_array = None

    print('Fetching game data')
    query = client.query(kind='Game_Model_Data')
    event_data = list(query.fetch())
    print('Game data fetched')

    data_array = np.zeros([len(game_column_names), len(event_data)])
    for idx, game in enumerate(event_data):
        for col in range(0, len(game_column_names)):
            data_array[col, idx] = game[game_column_names[col]]
    rows = len(event_data)
    event_data = None
    df_game = pd.DataFrame(data_array.transpose(), index=range(0, rows), columns=game_column_names)
    data_array = None


# Can only run from a local host due to using preposterous amounts of memory
def generate_data_frame_source_databases():
    print('Activating datastore')
    client = datastore.Client()

    print('Clearing player model data')
    query = client.query(kind='Player_Model_Data')
    old_player_model = list(query.fetch())
    for player in old_player_model:
        client.delete(player.key)

    print('Clearing game model data')
    query = client.query(kind='Game_Model_Data')
    old_game_model = list(query.fetch())
    for idx, game in enumerate(old_game_model):
        print('Deleting element ' + str(idx) + ' of ' + str(len(old_game_model)))
        client.delete(game.key)

    query = client.query(kind='Player_Statistic_Data')
    print('Fetching player statistic data')
    player_data = list(query.fetch())
    print('Player data fetched')

    print('Fetching event data')
    query = client.query(kind='Event_Data')
    event_data = list(query.fetch())
    print('Game data fetched')

    for idx, player in enumerate(player_data):
        entity = datastore.entity.Entity()
        entity.key = client.key('Player_Model_Data')
        entity[player_column_names[0]] = player.id
        entity[player_column_names[1]] = player['all_matches']['total_wins'] / player['all_matches']['total_matches']
        for col in range(2, len(player_column_names)):
            entity[player_column_names[col]] = player['all_matches']['overall'][player_column_names[col]]
        print('Writing player ' + str(idx) + ' of ' + str(len(player_data)))
        client.put(entity)

    # Use a dictionary for direct access to individual players' data
    player_data_dict = dict()
    for player in player_data:
        player_data_dict[player.key.id] = player

    for idx, game in enumerate(event_data):
        entity = datastore.entity.Entity()
        entity.key = client.key('Game_Model_Data')
        entity[game_column_names[0]] = game['homeTeam']
        entity[game_column_names[1]] = game['awayTeam']
        if game['winnerCode'] == 1:
            entity[game_column_names[2]] = 0
        else:
            entity[game_column_names[2]] = 1
        for a in range(0, 5):
            try:
                entity[game_column_names[3 + a]] = game['homeScore']['period' + str(a+1)]
            except KeyError:
                entity[game_column_names[3 + a]] = 0
        for b in range(0, 5):
            try:
                entity[game_column_names[8 + b]] = game['awayScore']['period' + str(b+1)]
            except KeyError:
                entity[game_column_names[8 + b]] = 0
        try:
            entity[game_column_names[13]] = game['awayScore']['normaltime'] + game['homeScore']['normaltime']
        except KeyError:
            entity[game_column_names[13]] = 3
        entity[game_column_names[14]] = 0
        for ab in range(3, 13):
            entity[game_column_names[14]] += entity[game_column_names[ab]]
        try:
            if game['homeScore']['normaltime'] > game['awayScore']['normaltime']:
                entity[game_column_names[15]] = 0
            else:
                entity[game_column_names[15]] = 1
        except KeyError:
            entity[game_column_names[15]] = 0
        entity[game_column_names[16]] = 0
        try:
            for ab in range(1, 6):
                if game['homeScore']['period' + str(ab)] > 11 or game['awayScore']['period' + str(ab)] > 11:
                    entity[game_column_names[16]] += 1
        except KeyError:
            pass
        player_columns = len(player_column_names)-1
        for col in range(17, 17 + player_columns):
            entity[game_column_names[col]] = \
                player_data_dict[int(game['homeTeam'])]['all_matches']['overall'][player_column_names[col - 17 + 1]]
        for col in range(17 + player_columns, 17 + 2 * player_columns):
            entity[game_column_names[col]] = \
                player_data_dict[int(game['homeTeam'])]['all_matches']['overall'][
                    player_column_names[col - 17 - player_columns + 1]]
        print('Writing game ' + str(idx) + ' of ' + str(len(event_data)))
        client.put(entity)


def initialize_who_win():
    # predict who wins
    global log_model_who_win

    label_who_win = df_game["who_win"]
    features = df_game[
        ["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
         "playerA_average_biggest_lead", "playerA_average_receiver_points_won",
         "playerA_average_service_points_won", "playerA_average_service_error",
         'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
         'playerA_average_receiver_points_lost', 'playerA_average_points',
         'playerB_win_rate', 'playerB_average_max_points_in_a_row',
         'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
         'playerB_average_receiver_points_won',
         'playerB_average_service_points_won', 'playerB_average_service_error',
         'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
         'playerB_average_receiver_points_lost', 'playerB_average_points']]

    x_train_who_win, x_test_who_win, y_train_who_win, y_test_who_win = train_test_split(features, label_who_win,
                                                                                        test_size=0.2)

    # create a simple, non-parameterized Logistic Regression model
    model_who_win = LogisticRegression(random_state=42)
    model_who_win.fit(x_train_who_win, y_train_who_win)

    y_pred_who_win = model_who_win.predict(x_test_who_win)

    # create complex Logistic Regression with max_iter=131
    log_model_who_win = LogisticRegression(max_iter=131, verbose=2, random_state=42)
    log_model_who_win.fit(x_train_who_win, y_train_who_win)
    y_pred_log_who_win = log_model_who_win.predict(x_test_who_win)

    with open('./data/log_model_who_win.pickle', 'wb') as f:
        pickle.dump(log_model_who_win, f)


def initialize_exact_number():
    global log_model_exact
    # Exact number of games initialization
    label_exact = df_game["Exact Number of Sets"]
    # prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
    features = df_game[
        ["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
         "playerA_average_biggest_lead", "playerA_average_receiver_points_won",
         "playerA_average_service_points_won", "playerA_average_service_error",
         'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
         'playerA_average_receiver_points_lost', 'playerA_average_points',
         'playerB_win_rate', 'playerB_average_max_points_in_a_row',
         'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
         'playerB_average_receiver_points_won',
         'playerB_average_service_points_won', 'playerB_average_service_error',
         'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
         'playerB_average_receiver_points_lost', 'playerB_average_points']]

    x_train_exact, x_test_exact, y_train_exact, y_test_exact = train_test_split(features, label_exact, test_size=0.2)

    # create a simple, non-parameterized Logistic Regression model
    model_exact = LogisticRegression(random_state=42)
    model_exact.fit(x_train_exact, y_train_exact)

    y_pred_exact = model_exact.predict(x_test_exact)

    # create complex Logistic Regression with max_iter=131
    log_model_exact = LogisticRegression(max_iter=131, verbose=2, random_state=42)
    log_model_exact.fit(x_train_exact, y_train_exact)
    y_pred_log_exact = log_model_exact.predict(x_test_exact)

    with open('./data/log_model_exact.pickle', 'wb') as f:
        pickle.dump(log_model_exact, f)


def initialize_first_winner():
    global log_model_first_winner
    # first game winner
    label_first_winner = df_game["First Game Winner"]
    # prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
    features = df_game[
        ["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
         "playerA_average_biggest_lead", "playerA_average_receiver_points_won",
         "playerA_average_service_points_won", "playerA_average_service_error",
         'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
         'playerA_average_receiver_points_lost', 'playerA_average_points',
         'playerB_win_rate', 'playerB_average_max_points_in_a_row',
         'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
         'playerB_average_receiver_points_won',
         'playerB_average_service_points_won', 'playerB_average_service_error',
         'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
         'playerB_average_receiver_points_lost', 'playerB_average_points']]

    x_train_first_winner, x_test_first_winner, y_train_first_winner, y_test_first_winner = train_test_split(features,
                                                                                                            label_first_winner,
                                                                                                            test_size=0.2)

    model_first_winner = LogisticRegression(random_state=42)
    model_first_winner.fit(x_train_first_winner, y_train_first_winner)
    y_pred_first_winner = model_first_winner.predict(x_test_first_winner)

    # create complex Logistic Regression with max_iter=131
    log_model_first_winner = LogisticRegression(max_iter=131, verbose=2, random_state=42)
    log_model_first_winner.fit(x_train_first_winner, y_train_first_winner)
    y_pred_log_first_winner = log_model_first_winner.predict(x_test_first_winner)

    with open('./data/log_model_first_winner.pickle', 'wb') as f:
        pickle.dump(log_model_first_winner, f)


# initialize extra point prediction
def initialize_extra_point():
    global log_model_extra_point
    label_extra_point = df_game["Sets Decided by Extra Points"]
    # prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
    features = df_game[
        ["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
         "playerA_average_biggest_lead", "playerA_average_receiver_points_won",
         "playerA_average_service_points_won", "playerA_average_service_error",
         'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
         'playerA_average_receiver_points_lost', 'playerA_average_points',
         'playerB_win_rate', 'playerB_average_max_points_in_a_row',
         'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
         'playerB_average_receiver_points_won',
         'playerB_average_service_points_won', 'playerB_average_service_error',
         'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
         'playerB_average_receiver_points_lost', 'playerB_average_points']]

    x_train_extra_point, x_test_extra_point, y_train_extra_point, y_test_extra_point = train_test_split(features,
                                                                                                        label_extra_point,
                                                                                                        test_size=0.2)

    model_extra_point = LogisticRegression(random_state=42)
    model_extra_point.fit(x_train_extra_point, y_train_extra_point)

    y_pred_extra_point = model_extra_point.predict(x_test_extra_point)

    # create complex Logistic Regression with max_iter=131
    log_model_extra_point = LogisticRegression(max_iter=131, verbose=2, random_state=42)
    log_model_extra_point.fit(x_train_extra_point, y_train_extra_point)
    y_pred_log_extra_point = log_model_extra_point.predict(x_test_extra_point)

    with open('./data/log_model_extra_point.pickle', 'wb') as f:
        pickle.dump(log_model_extra_point, f)


def initialize_total_points():
    # Predict Total Points
    global b_coef
    # Training Model
    tmp_list = [0] * 17551

    for i in range(0, 17551):
        tmp_total = int(df_game.iat[i, 14])
        # print("tmp_total is ", tmp_total)
        avg_attri = 0.0
        tmp_ele = [0, 0]
        for x in range(17, 39):
            avg_attri = avg_attri + float(df_game.iat[i, x] * 10000)
            # tmp_ele = [avg_attri,tmp_total]
        tmp_ele = [avg_attri, tmp_total]
        tmp_list[i] = tmp_ele

    x_array = [0] * 17551
    y_array = [0] * 17551
    for i in range(0, 17551):
        x_array[i] = tmp_list[i][0]
        y_array[i] = tmp_list[i][1]

    x_array = np.array(x_array)
    y_array = np.array(y_array)
    b_coef = estimate_coef(x_array, y_array)

    with open('./data/b_coef.pickle', 'wb') as f:
        pickle.dump(b_coef, f)


def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return b_0, b_1


if __name__ == '__main__':
    generate_models()
