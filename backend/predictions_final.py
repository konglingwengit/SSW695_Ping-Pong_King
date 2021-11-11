import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from pprint import pprint
import matplotlib.pyplot as plt
from sklearn import linear_model
import math
from google.cloud import datastore

df_game = None
df_player = None
log_model_who_win = None
log_model_exact = None
log_model_first_winner = None
log_model_extra_point = None
b_coef = None


def initialize_predictions():
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

    player_column_names = ['playerID', 'win_rate', 'average_max_points_in_a_row', 'average_service_points_lost',
                           'average_biggest_lead', 'average_receiver_points_won', 'average_service_points_won',
                           'average_service_error', 'average_comeback_loss', 'average_comeback_to_win',
                           'average_receiver_points_lost', 'average_points']

    print('Activating datastore')
    client = datastore.Client()

    query = client.query(kind='Player_Statistic_Data')
    print('Fetching player data')
    player_data = list(query.fetch())
    print('Player data fetched')

    data_array = np.zeros([len(player_column_names), len(player_data)])
    for idx, player in enumerate(player_data):
        data_array[0, idx] = player.id
        data_array[1, idx] = player['all_matches']['total_wins'] / player['all_matches']['total_matches']
        for col in range(2, len(player_column_names)):
            data_array[col, idx] = player['all_matches']['overall'][player_column_names[col]]
    df_player = pd.DataFrame(data_array.transpose(), index=range(0, len(player_data)), columns=player_column_names)

    # Use a dictionary for direct access to individual players' data
    player_data_dict = dict()
    for player in player_data:
        player_data_dict[player.key.id] = player

    print('Fetching game data')
    query = client.query(kind='Event_Data')
    event_data = list(query.fetch())
    print('Game data fetched')

    game_column_names = ['playerA', 'playerB', 'who_win', 'Aset1', 'Aset2', 'Aset3', 'Aset4', 'Aset5',
                         'Bset1', 'Bset2', 'Bset3', 'Bset4', 'Bset5', 'Exact Number of Sets', 'Total Points',
                         'First Game Winner', 'Sets Decided by Extra Points']
    player_list = ['playerA', 'playerB']
    for player in player_list:
        for idx, column in enumerate(player_column_names):
            if idx != 0:
                game_column_names.append(player + '_' + column)

    data_array = np.zeros([len(game_column_names), len(event_data)])
    for idx, game in enumerate(event_data):
        data_array[0, idx] = game['homeTeam']
        data_array[1, idx] = game['awayTeam']
        if game['winnerCode'] == 1:
            data_array[2, idx] = 0
        else:
            data_array[2, idx] = 1
        for a in range(0, 5):
            try:
                data_array[3 + a, idx] = game['homeScore']['period' + str(a)]
            except KeyError:
                data_array[3 + a, idx] = 0
        for b in range(0, 5):
            try:
                data_array[8 + b, idx] = game['awayScore']['period' + str(b)]
            except KeyError:
                data_array[8 + b, idx] = 0
        try:
            data_array[13, idx] = game['awayScore']['normaltime'] + game['homeScore']['normaltime']
        except KeyError:
            data_array[13, idx] = 3
        for ab in range(3, 13):
            data_array[14, idx] += data_array[ab, idx]
        try:
            if game['homeScore']['normaltime'] > game['awayScore']['normaltime']:
                data_array[15, idx] = 0
            else:
                data_array[15, idx] = 1
        except KeyError:
            data_array[15, idx] = 0
        try:
            for ab in range(1, 6):
                if game['homeScore']['period' + str(ab)] > 11 or game['awayScore']['period' + str(ab)] > 11:
                    data_array[16, idx] += 1
        except KeyError:
            pass
        player_columns = len(player_column_names)-1
        for col in range(17, 17 + player_columns):
            data_array[col, idx] = \
                player_data_dict[int(game['homeTeam'])]['all_matches']['overall'][player_column_names[col - 17 + 1]]
        for col in range(17 + player_columns, 17 + 2 * player_columns):
            data_array[col, idx] = \
                player_data_dict[int(game['homeTeam'])]['all_matches']['overall'][
                    player_column_names[col - 17 - player_columns + 1]]

    df_game = pd.DataFrame(data_array.transpose(), index=range(0, len(event_data)), columns=game_column_names)


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


# Predict Who Win
def prediction_who_win(playerA_ID, playerB_ID):
    table_a = df_player[(df_player['playerID'] == playerA_ID)]
    table_b = df_player[(df_player['playerID'] == playerB_ID)]
    # if can't find player info
    if (table_a.count == 0 or table_b.count == 0):
        msg = "Invalid Player"
        return msg
    tmp_ab = pd.DataFrame()
    tmp_ab_col = ['playerA_win_rate',
                  'playerA_average_max_points_in_a_row',
                  'playerA_average_service_points_lost',
                  'playerA_average_biggest_lead',
                  'playerA_average_receiver_points_won',
                  'playerA_average_service_points_won',
                  'playerA_average_service_error',
                  'playerA_average_comeback_loss',
                  'playerA_average_comeback_to_win',
                  'playerA_average_receiver_points_lost',
                  'playerA_average_points',
                  'playerB_win_rate',
                  'playerB_average_max_points_in_a_row',
                  'playerB_average_service_points_lost',
                  'playerB_average_biggest_lead',
                  'playerB_average_receiver_points_won',
                  'playerB_average_service_points_won',
                  'playerB_average_service_error',
                  'playerB_average_comeback_loss',
                  'playerB_average_comeback_to_win',
                  'playerB_average_receiver_points_lost',
                  'playerB_average_points']

    tmp_ab_data = [0] * 22
    for x in range(0, 11):
        tmp_ab_data[x] = table_a.iat[0, x + 1]
    for x in range(11, 22):
        tmp_ab_data[x] = table_b.iat[0, x - 10]

    pred_df = pd.DataFrame([tmp_ab_data], columns=tmp_ab_col)
    pred_ab = log_model_who_win.predict(pred_df)

    if (int(pred_ab[0]) == 0):
        return playerA_ID
    else:
        return playerB_ID


# Predict Exact Number of Games
def prediction_exact(playerA_ID, playerB_ID):
    table_a = df_player[(df_player['playerID'] == playerA_ID)]
    table_b = df_player[(df_player['playerID'] == playerB_ID)]
    # if can't find player info
    if (table_a.count == 0 or table_b.count == 0):
        msg = "Invalid Player"
        return msg
    tmp_ab = pd.DataFrame()
    tmp_ab_col = ['playerA_win_rate',
                  'playerA_average_max_points_in_a_row',
                  'playerA_average_service_points_lost',
                  'playerA_average_biggest_lead',
                  'playerA_average_receiver_points_won',
                  'playerA_average_service_points_won',
                  'playerA_average_service_error',
                  'playerA_average_comeback_loss',
                  'playerA_average_comeback_to_win',
                  'playerA_average_receiver_points_lost',
                  'playerA_average_points',
                  'playerB_win_rate',
                  'playerB_average_max_points_in_a_row',
                  'playerB_average_service_points_lost',
                  'playerB_average_biggest_lead',
                  'playerB_average_receiver_points_won',
                  'playerB_average_service_points_won',
                  'playerB_average_service_error',
                  'playerB_average_comeback_loss',
                  'playerB_average_comeback_to_win',
                  'playerB_average_receiver_points_lost',
                  'playerB_average_points']

    tmp_ab_data = [0] * 22
    for x in range(0, 11):
        tmp_ab_data[x] = table_a.iat[0, x + 1]
    for x in range(11, 22):
        tmp_ab_data[x] = table_b.iat[0, x - 10]

    pred_df = pd.DataFrame([tmp_ab_data], columns=tmp_ab_col)
    pred_ab = log_model_exact.predict(pred_df)

    return pred_ab[0]


# First Game Winner
def prediction_first_winner(playerA_ID, playerB_ID):
    table_a = df_player[(df_player['playerID'] == playerA_ID)]
    table_b = df_player[(df_player['playerID'] == playerB_ID)]
    # if can't find player info
    if (table_a.count == 0 or table_b.count == 0):
        msg = "Invalid Player"
        return msg
    tmp_ab = pd.DataFrame()
    tmp_ab_col = ['playerA_win_rate',
                  'playerA_average_max_points_in_a_row',
                  'playerA_average_service_points_lost',
                  'playerA_average_biggest_lead',
                  'playerA_average_receiver_points_won',
                  'playerA_average_service_points_won',
                  'playerA_average_service_error',
                  'playerA_average_comeback_loss',
                  'playerA_average_comeback_to_win',
                  'playerA_average_receiver_points_lost',
                  'playerA_average_points',
                  'playerB_win_rate',
                  'playerB_average_max_points_in_a_row',
                  'playerB_average_service_points_lost',
                  'playerB_average_biggest_lead',
                  'playerB_average_receiver_points_won',
                  'playerB_average_service_points_won',
                  'playerB_average_service_error',
                  'playerB_average_comeback_loss',
                  'playerB_average_comeback_to_win',
                  'playerB_average_receiver_points_lost',
                  'playerB_average_points']

    tmp_ab_data = [0] * 22
    for x in range(0, 11):
        tmp_ab_data[x] = table_a.iat[0, x + 1]
    for x in range(11, 22):
        tmp_ab_data[x] = table_b.iat[0, x - 10]

    pred_df = pd.DataFrame([tmp_ab_data], columns=tmp_ab_col)
    pred_ab = log_model_exact.predict(pred_df)

    if (int(pred_ab[0]) == 0):
        return playerA_ID
    else:
        return playerB_ID


# Sets Decided By Extra Point
def prediction_extra_point(playerA_ID, playerB_ID):
    table_a = df_player[(df_player['playerID'] == playerA_ID)]
    table_b = df_player[(df_player['playerID'] == playerB_ID)]
    # if can't find player info
    if (table_a.count == 0 or table_b.count == 0):
        msg = "Invalid Player"
        return msg
    tmp_ab = pd.DataFrame()
    tmp_ab_col = ['playerA_win_rate',
                  'playerA_average_max_points_in_a_row',
                  'playerA_average_service_points_lost',
                  'playerA_average_biggest_lead',
                  'playerA_average_receiver_points_won',
                  'playerA_average_service_points_won',
                  'playerA_average_service_error',
                  'playerA_average_comeback_loss',
                  'playerA_average_comeback_to_win',
                  'playerA_average_receiver_points_lost',
                  'playerA_average_points',
                  'playerB_win_rate',
                  'playerB_average_max_points_in_a_row',
                  'playerB_average_service_points_lost',
                  'playerB_average_biggest_lead',
                  'playerB_average_receiver_points_won',
                  'playerB_average_service_points_won',
                  'playerB_average_service_error',
                  'playerB_average_comeback_loss',
                  'playerB_average_comeback_to_win',
                  'playerB_average_receiver_points_lost',
                  'playerB_average_points']

    tmp_ab_data = [0] * 22
    for x in range(0, 11):
        tmp_ab_data[x] = table_a.iat[0, x + 1]
    for x in range(11, 22):
        tmp_ab_data[x] = table_b.iat[0, x - 10]

    pred_df = pd.DataFrame([tmp_ab_data], columns=tmp_ab_col)
    pred_ab = log_model_extra_point.predict(pred_df)

    return pred_ab[0]


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

    return (b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


def prediction_total_points(playerA_ID, playerB_ID):
    table_a = df_player[(df_player['playerID'] == playerA_ID)]
    table_b = df_player[(df_player['playerID'] == playerB_ID)]
    # if can't find player info
    if (table_a.count == 0 or table_b.count == 0):
        msg = "Invalid Player"
        return msg
    sum_a = 0.0
    sum_b = 0.0
    sum_ab = 0.0

    for i in range(1, 12):
        sum_a = sum_a + float(table_a.iat[0, i]) * 10000
        sum_b = sum_b + float(table_b.iat[0, i]) * 10000

    sum_ab = sum_a + sum_b
    pred_total_points = sum_ab * b_coef[1] + b_coef[0]
    pred_total_floor = math.floor(pred_total_points)
    diff = (pred_total_points - pred_total_floor) * 50

    return math.floor(pred_total_points + diff)


def prediction_all(playerA_ID, playerB_ID):
    res = [prediction_who_win(playerA_ID, playerB_ID),
           prediction_exact(playerA_ID, playerB_ID),
           prediction_total_points(playerA_ID, playerB_ID),
           prediction_first_winner(playerA_ID, playerB_ID),
           prediction_extra_point(playerA_ID, playerB_ID)]
    return res


if __name__ == '__main__':
    initialize_predictions()
    prediction_all(345226, 345227)
