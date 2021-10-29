import json
from google.cloud import datastore

client = None


def predict(a_id, b_id):
    global client
    if client is None:
        client = datastore.Client()
    query = client.query(kind='Event_Data')
    query.add_filter('homeTeam', '=', a_id)
    query.add_filter('awayTeam', '=', b_id)
    player_a_home = list(query.fetch())
    query = client.query(kind='Event_Data')
    query.add_filter('homeTeam', '=', b_id)
    query.add_filter('awayTeam', '=', a_id)
    player_b_home = list(query.fetch())
    all_games = player_a_home + player_b_home

    A_played = len(all_games)
    A_won = 0
    B_played = len(all_games)
    B_won = 0
    for i in all_games:
        if i['winnerCode'] == 1:
            if a_id == i['homeTeam']:
                A_won = A_won + 1
            else:
                B_won = B_won + 1
        else:
            if a_id == i['awayTeam']:
                A_won = A_won + 1
            else:
                B_won = B_won + 1

    try:
        A_win_rate = (A_played / A_won) * 100
        B_win_rate = (B_played / B_won) * 100

        probability_A = (A_win_rate / (A_win_rate + B_win_rate)) * 100
        probability_B = (B_win_rate / (A_win_rate + B_win_rate)) * 100
    except ZeroDivisionError:
        probability_A = 50
        probability_B = 50

    print(f"Team A's({a_id}) winning chances are {probability_A}%, and B's({b_id}) chances are {probability_B}%")


if __name__ == '__main__':
    while True:
        teamA = input("PLease Enter 1st player ID: ")
        teamB = input("PLease Enter 2nd player ID: ")
        try:
            predict(int(teamA), int(teamB))
        except ValueError:
            print("invlaid ID's")

        check = input("please enter y to exit : ")
        if check == 'y':
            break
