import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from google.cloud import datastore
import pickle
from predictions_final import initialize_columns
import matplotlib.pyplot as plt


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
    global player_column_names
    global game_column_names
    player_column_names, game_column_names = initialize_columns()

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
        total_points = 0
        for ab in range(3, 13):
            total_points += entity[game_column_names[ab]]
        # Change total points from an actual sum to 0 if under 78.5, 1 if over
        if total_points < 78.5:
            entity[game_column_names[14]] = 0
        else:
            entity[game_column_names[14]] = 1
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
                player_data_dict[int(game['awayTeam'])]['all_matches']['overall'][
                    player_column_names[col - 17 - player_columns + 1]]
        print('Writing game ' + str(idx) + ' of ' + str(len(event_data)))
        client.put(entity)


def initialize_who_win():
    # predict who wins
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

    label_total_points = df_game["Total Points"]
    # prediction_fields = df_game[["who_win","Exact Number of Sets","Total Points","First Game Winner","Sets Decided by Extra Points"]]
    features = df_game[
        ["playerA_win_rate", "playerA_average_max_points_in_a_row", "playerA_average_service_points_lost",
         "playerA_average_biggest_lead", "playerA_average_receiver_points_won", "playerA_average_service_points_won",
         "playerA_average_service_error", 'playerA_average_comeback_loss', 'playerA_average_comeback_to_win',
         'playerA_average_receiver_points_lost', 'playerA_average_points',
         'playerB_win_rate', 'playerB_average_max_points_in_a_row',
         'playerB_average_service_points_lost', 'playerB_average_biggest_lead',
         'playerB_average_receiver_points_won',
         'playerB_average_service_points_won', 'playerB_average_service_error',
         'playerB_average_comeback_loss', 'playerB_average_comeback_to_win',
         'playerB_average_receiver_points_lost', 'playerB_average_points']]

    x_train_total_points, x_test_total_points, y_train_total_points, y_test_total_points = train_test_split(features,
                                                                                                            label_total_points,
                                                                                                            test_size=0.2)

    model_total_points = LogisticRegression(random_state=42)
    model_total_points.fit(x_train_total_points, y_train_total_points)

    y_pred_total_points = model_total_points.predict(x_test_total_points)

    # create complex Logistic Regression with max_iter=131
    log_model_total_points = LogisticRegression(max_iter=131, verbose=2, random_state=42)
    log_model_total_points.fit(x_train_total_points, y_train_total_points)
    y_pred_log_total_points = log_model_total_points.predict(x_test_total_points)

    with open('./data/log_model_total_points.pickle', 'wb') as f:
        pickle.dump(log_model_total_points, f)


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


if __name__ == '__main__':
    generate_models()
