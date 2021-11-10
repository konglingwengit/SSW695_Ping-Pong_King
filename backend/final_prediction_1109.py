import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from pprint import pprint

#inite df
df_game = pd.read_csv(r'/Users/lingwenkong/Downloads/ML_table_tennis/final_table.csv')
df_player = pd.read_csv(r'/Users/lingwenkong/Downloads/ML_table_tennis/player_table.csv')

def get_avg_stats_last_n_games(player_id, game_table, n):
    prev_game_df = game_table[(game_table['playerA']== int(player_id)) | (game_table['PlayerB']== int(player_id))].tail(n)
    return prev_game_df

# predict who wins
label_who_win = df_game["who_win"]
features = df_game[["playerA_win_rate","playerA_average_max_points_in_a_row","playerA_average_service_points_lost","playerA_average_biggest_lead","playerA_average_receiver_points_won","playerA_average_service_points_won","playerA_average_service_error",'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
       'playerA_average_receiver_points_lost', 'playerA_average_points',
       'playerB_win_rate', 'playerB_average_max_points_in_a_row',
       'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
       'playerB_average_receiver_points_won',
       'playerB_average_service_points_won', 'playerB_average_service_error',
       'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
       'playerB_average_receiver_points_lost', 'playerB_average_points']]

x_train_who_win, x_test_who_win, y_train_who_win, y_test_who_win = train_test_split(features, label_who_win, test_size = 0.2)


# create a simple, non-parameterized Logistic Regression model
model_who_win = LogisticRegression(random_state=42)
model_who_win.fit(x_train_who_win, y_train_who_win)

y_pred_who_win = model_who_win.predict(x_test_who_win)

# create complex Logistic Regression with max_iter=131 
log_model_who_win = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model_who_win.fit(x_train_who_win, y_train_who_win)
y_pred_log_who_win = log_model_who_win.predict(x_test_who_win)
#print(metrics.accuracy_score(y_test_who_win, y_pred_log_who_win))

#Predict Who Win
def prediction_who_win(playerA_ID, playerB_ID, player_table):
    
    table_a = player_table[(player_table['playerID']== str(playerA_ID))]
    table_b = player_table[(player_table['playerID']== str(playerB_ID))]
    #if can't find player info
    if(table_a.count == 0 or table_b.count == 0):
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

    tmp_ab_data = [0]*22
    for x in range(0,11):
        tmp_ab_data[x] = table_a.iat[0,x+1]
    for x in range(11,22):
        tmp_ab_data[x] = table_b.iat[0,x-10]

    pred_df = pd.DataFrame([tmp_ab_data], columns = tmp_ab_col)
    pred_ab = log_model_who_win.predict(pred_df)

    if(int(pred_ab[0]) == 0):
        return playerA_ID
    else:
        return playerB_ID

#prediction_who_win(345228,345232,df_player)

#Predict Exact Number of Games
label_exact = df_game["Exact Number of Sets"]
#prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate","playerA_average_max_points_in_a_row","playerA_average_service_points_lost","playerA_average_biggest_lead","playerA_average_receiver_points_won","playerA_average_service_points_won","playerA_average_service_error",'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
       'playerA_average_receiver_points_lost', 'playerA_average_points',
       'playerB_win_rate', 'playerB_average_max_points_in_a_row',
       'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
       'playerB_average_receiver_points_won',
       'playerB_average_service_points_won', 'playerB_average_service_error',
       'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
       'playerB_average_receiver_points_lost', 'playerB_average_points']]


x_train_exact, x_test_exact, y_train_exact, y_test_exact = train_test_split(features, label_exact, test_size = 0.2)


# create a simple, non-parameterized Logistic Regression model
model_exact = LogisticRegression(random_state=42)
model_exact.fit(x_train_exact, y_train_exact)

y_pred_exact = model_exact.predict(x_test_exact)

# create complex Logistic Regression with max_iter=131 
log_model_exact = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model_exact.fit(x_train_exact, y_train_exact)
y_pred_log_exact = log_model_exact.predict(x_test_exact)

def prediction_exact(playerA_ID, playerB_ID, player_table):
    
    table_a = player_table[(player_table['playerID']== str(playerA_ID))]
    table_b = player_table[(player_table['playerID']== str(playerB_ID))]
    #if can't find player info
    if(table_a.count == 0 or table_b.count == 0):
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

    tmp_ab_data = [0]*22
    for x in range(0,11):
        tmp_ab_data[x] = table_a.iat[0,x+1]
    for x in range(11,22):
        tmp_ab_data[x] = table_b.iat[0,x-10]

    pred_df = pd.DataFrame([tmp_ab_data], columns = tmp_ab_col)
    pred_ab = log_model_exact.predict(pred_df)

    return pred_ab[0]

#prediction_exact(345228,345232,df_player)


#First Game Winner
label_first_winner = df_game["First Game Winner"]
#prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate","playerA_average_max_points_in_a_row","playerA_average_service_points_lost","playerA_average_biggest_lead","playerA_average_receiver_points_won","playerA_average_service_points_won","playerA_average_service_error",'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
       'playerA_average_receiver_points_lost', 'playerA_average_points',
       'playerB_win_rate', 'playerB_average_max_points_in_a_row',
       'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
       'playerB_average_receiver_points_won',
       'playerB_average_service_points_won', 'playerB_average_service_error',
       'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
       'playerB_average_receiver_points_lost', 'playerB_average_points']]


x_train_first_winner, x_test_first_winner, y_train_first_winner, y_test_first_winner = train_test_split(features, label_first_winner, test_size = 0.2)

model_first_winner = LogisticRegression(random_state=42)
model_first_winner.fit(x_train_exact, y_train_exact)

y_pred_first_winner = model_first_winner.predict(x_test_first_winner)

# create complex Logistic Regression with max_iter=131 
log_model_first_winner = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model_first_winner.fit(x_train_first_winner, y_train_first_winner)
y_pred_log_first_winner = log_model_first_winner.predict(x_test_first_winner)
#y_pred_log_first_winner[0]

def prediction_first_winner(playerA_ID, playerB_ID, player_table):
    
    table_a = player_table[(player_table['playerID']== str(playerA_ID))]
    table_b = player_table[(player_table['playerID']== str(playerB_ID))]
    #if can't find player info
    if(table_a.count == 0 or table_b.count == 0):
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

    tmp_ab_data = [0]*22
    for x in range(0,11):
        tmp_ab_data[x] = table_a.iat[0,x+1]
    for x in range(11,22):
        tmp_ab_data[x] = table_b.iat[0,x-10]

    pred_df = pd.DataFrame([tmp_ab_data], columns = tmp_ab_col)
    pred_ab = log_model_exact.predict(pred_df)
    
    if(int(pred_ab[0]) == 0):
        return playerA_ID
    else:
        return playerB_ID
#prediction_first_winner(345228,345232,df_player)


#Sets Decided By Extra Point
label_extra_point = df_game["Sets Decided by Extra Points"]
#prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
features = df_game[["playerA_win_rate","playerA_average_max_points_in_a_row","playerA_average_service_points_lost","playerA_average_biggest_lead","playerA_average_receiver_points_won","playerA_average_service_points_won","playerA_average_service_error",'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
       'playerA_average_receiver_points_lost', 'playerA_average_points',
       'playerB_win_rate', 'playerB_average_max_points_in_a_row',
       'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
       'playerB_average_receiver_points_won',
       'playerB_average_service_points_won', 'playerB_average_service_error',
       'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
       'playerB_average_receiver_points_lost', 'playerB_average_points']]

x_train_extra_point, x_test_extra_point, y_train_extra_point, y_test_extra_point = train_test_split(features, label_extra_point, test_size = 0.2)

model_extra_point = LogisticRegression(random_state=42)
model_extra_point.fit(x_train_extra_point, y_train_extra_point)

y_pred_extra_point = model_extra_point.predict(x_test_extra_point)

# create complex Logistic Regression with max_iter=131 
log_model_extra_point = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model_extra_point.fit(x_train_extra_point, y_train_extra_point)
y_pred_log_extra_point = log_model_extra_point.predict(x_test_extra_point)
#y_pred_log_first_winner[0]

def prediction_extra_point(playerA_ID, playerB_ID, player_table):
    
    table_a = player_table[(player_table['playerID']== str(playerA_ID))]
    table_b = player_table[(player_table['playerID']== str(playerB_ID))]
    #if can't find player info
    if(table_a.count == 0 or table_b.count == 0):
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

    tmp_ab_data = [0]*22
    for x in range(0,11):
        tmp_ab_data[x] = table_a.iat[0,x+1]
    for x in range(11,22):
        tmp_ab_data[x] = table_b.iat[0,x-10]

    pred_df = pd.DataFrame([tmp_ab_data], columns = tmp_ab_col)
    pred_ab = log_model_extra_point.predict(pred_df)
    
    return pred_ab[0]
#prediction_extra_point(345228,345232,df_player)

def prediction_all(playerA_ID, playerB_ID, player_table):
    res = [prediction_who_win(playerA_ID, playerB_ID, player_table),
          prediction_exact(playerA_ID, playerB_ID, player_table),
           prediction_first_winner(playerA_ID, playerB_ID, player_table),
           prediction_extra_point(playerA_ID, playerB_ID, player_table)]
    return res

#prediction_all(345228,345232,df_player)
          
