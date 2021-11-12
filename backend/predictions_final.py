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
import pickle

df_player = None
log_model_who_win = None
log_model_exact = None
log_model_first_winner = None
log_model_extra_point = None
b_coef = None
player_column_names = None
game_column_names = None


def initialize_predictions():
    global player_column_names
    global game_column_names
    player_column_names, game_column_names = initialize_columns()
    initialize_player_frame()
    initialize_data_from_machine_models()


def initialize_data_from_machine_models():
    global b_coef
    global log_model_who_win
    global log_model_exact
    global log_model_first_winner
    global log_model_extra_point
    with open('./data/log_model_who_win.pickle', 'rb') as f:
        log_model_who_win = pickle.load(f)
    with open('./data/log_model_exact.pickle', 'rb') as f:
        log_model_exact = pickle.load(f)
    with open('./data/log_model_first_winner.pickle', 'rb') as f:
        log_model_first_winner = pickle.load(f)
    with open('./data/log_model_extra_point.pickle', 'rb') as f:
        log_model_extra_point = pickle.load(f)
    with open('./data/b_coef.pickle', 'rb') as f:
        b_coef = pickle.load(f)


def initialize_columns():

    player_columns = ['playerID', 'win_rate', 'average_max_points_in_a_row', 'average_service_points_lost',
                           'average_biggest_lead', 'average_receiver_points_won', 'average_service_points_won',
                           'average_service_error', 'average_comeback_loss', 'average_comeback_to_win',
                           'average_receiver_points_lost', 'average_points']


    game_columns = ['playerA', 'playerB', 'who_win', 'Aset1', 'Aset2', 'Aset3', 'Aset4', 'Aset5',
                         'Bset1', 'Bset2', 'Bset3', 'Bset4', 'Bset5', 'Exact Number of Sets', 'Total Points',
                         'First Game Winner', 'Sets Decided by Extra Points']
    player_list = ['playerA', 'playerB']
    for player in player_list:
        for idx, column in enumerate(player_columns):
            if idx != 0:
                game_columns.append(player + '_' + column)

    return player_columns, game_columns


def initialize_player_frame():
    # init. df
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


# Predict Who Win
def prediction_who_win(playerA_ID, playerB_ID):
    if df_player is None:
        initialize_predictions()

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
    if df_player is None:
        initialize_predictions()

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
    if df_player is None:
        initialize_predictions()

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
    if df_player is None:
        initialize_predictions()

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
    if df_player is None:
        initialize_predictions()

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
