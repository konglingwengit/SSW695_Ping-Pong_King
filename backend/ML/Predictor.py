import json
import pandas as pd


def Predict(A_id, B_id):
    file = pd.read_excel('report.xlsx')
    file = file.to_json(orient='records')
    data = json.loads(file)

    A_played = 0
    A_won = 0
    B_played = 0
    B_won = 0
    for i in data:
        if A_id in [i["Player_A_ID"], i["Player_B_ID"]]:
            if i["who_won"] == A_id:
                A_won += 1
            A_played += 1
        if B_id in [i["Player_A_ID"], i["Player_B_ID"]]:
            if i["who_won"] == B_id:
                B_won += 1
            B_played += 1
    try:
        A_win_rate = (A_played / A_won) * 100
        B_win_rate = (B_played / B_won) * 100

        probability_A = (A_win_rate / (A_win_rate + B_win_rate)) * 100
        probability_B = (B_win_rate / (A_win_rate + B_win_rate)) * 100
    except ZeroDivisionError:
        probability_A = 50
        probability_B = 50

    print(f"Team A's({A_id}) winning chances are {probability_A}%, and B's({B_id}) chances are {probability_B}%")


if __name__ == '__main__':
    while True:
        teamA = input("PLease Enter 1st player ID: ")
        teamB = input("PLease Enter 2nd player ID: ")
        try:
            Predict(int(teamA), int(teamB))
        except ValueError:
            print("invlaid ID's")

        check = input("please enter y to exit : ")
        if check == 'y':
            break
