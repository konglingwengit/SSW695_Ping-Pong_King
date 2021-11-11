import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from pprint import pprint
import matplotlib.pyplot as plt
from sklearn import linear_model
import math

# init. df
df_game = pd.read_csv(r'final_table.csv')
df_player = pd.read_csv(r'player_table.csv')

# predict who wins
label_who_win = df_game["who_win"]
features = df_game[["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
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


# print(metrics.accuracy_score(y_test_who_win, y_pred_log_who_win))

# Predict Who Win
def prediction_who_win(playerA_ID, playerB_ID, player_table):
    table_a = player_table[(player_table['playerID'] == str(playerA_ID))]
    table_b = player_table[(player_table['playerID'] == str(playerB_ID))]
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


# prediction_who_win(345228,345232,df_player)

# Predict Exact Number of Games
label_exact = df_game["Exact Number of Sets"]
# prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
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


def prediction_exact(playerA_ID, playerB_ID, player_table):
    table_a = player_table[(player_table['playerID'] == str(playerA_ID))]
    table_b = player_table[(player_table['playerID'] == str(playerB_ID))]
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


# prediction_exact(345228,345232,df_player)


# First Game Winner
label_first_winner = df_game["First Game Winner"]
# prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
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
model_first_winner.fit(x_train_exact, y_train_exact)

y_pred_first_winner = model_first_winner.predict(x_test_first_winner)

# create complex Logistic Regression with max_iter=131
log_model_first_winner = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model_first_winner.fit(x_train_first_winner, y_train_first_winner)
y_pred_log_first_winner = log_model_first_winner.predict(x_test_first_winner)


# y_pred_log_first_winner[0]

def prediction_first_winner(playerA_ID, playerB_ID, player_table):
    table_a = player_table[(player_table['playerID'] == str(playerA_ID))]
    table_b = player_table[(player_table['playerID'] == str(playerB_ID))]
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


# prediction_first_winner(345228,345232,df_player)


# Sets Decided By Extra Point
label_extra_point = df_game["Sets Decided by Extra Points"]
# prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
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


# y_pred_log_first_winner[0]

def prediction_extra_point(playerA_ID, playerB_ID, player_table):
    table_a = player_table[(player_table['playerID'] == str(playerA_ID))]
    table_b = player_table[(player_table['playerID'] == str(playerB_ID))]
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


# prediction_extra_point(345228,345232,df_player)

# Predict Total Points
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


x_array = np.array(x_array)
y_array = np.array(y_array)
b_coef = estimate_coef(x_array, y_array)


# plot_regression_line(x_array, y_array, b_coef)

def prediction_total_points(playerA_ID, playerB_ID, player_table):
    table_a = player_table[(player_table['playerID'] == str(playerA_ID))]
    table_b = player_table[(player_table['playerID'] == str(playerB_ID))]
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


def prediction_all(playerA_ID, playerB_ID, player_table):
    res = [prediction_who_win(playerA_ID, playerB_ID, player_table),
           prediction_exact(playerA_ID, playerB_ID, player_table),
           prediction_total_points(playerA_ID, playerB_ID, player_table),
           prediction_first_winner(playerA_ID, playerB_ID, player_table),
           prediction_extra_point(playerA_ID, playerB_ID, player_table)]
    return res

# print(prediction_all(345228,345232,df_player))
# print(prediction_all(345228,345230,df_player))
# print(prediction_all(345230,345232,df_player))
# print(prediction_all(345228,345226,df_player))
# print(prediction_all(345226,345232,df_player))
# print(prediction_all(345226,345230,df_player))
