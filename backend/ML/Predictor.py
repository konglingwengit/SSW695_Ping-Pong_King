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
    A_win_rate = 0
    B_win_rate = 0
    for i in data:
        if A_id == int(i["Player_A_ID"]):
            for j in range(2,5):
                setpointa = i[f'Set{str(j)}_A']
                setpointb = i[f'Set{str(j)}_B']
                if setpointa == '-' or setpointb == '-':
                    break
                if int(setpointa) > int(setpointb):
                    A_won+=1
                A_played+=1
        elif A_id == int(i["Player_B_ID"]):
            for j in range(2,5):
                setpointa = i[f'Set{str(j)}_A']
                setpointb = i[f'Set{str(j)}_B']
                if setpointa == '-' or setpointb == '-':
                    break
                if int(setpointb) > int(setpointa):
                    A_won+=1
                A_played+=1

        if B_id == int(i["Player_A_ID"]):
            for j in range(2,5):
                setpointa = i[f'Set{str(j)}_A']
                setpointb = i[f'Set{str(j)}_B']
                if setpointa == '-' or setpointb == '-':
                    break
                if int(setpointa) > int(setpointb):
                    B_won+=1
                B_played+=1
        elif B_id == int(i["Player_B_ID"]):
            for j in range(2,5):
                setpointa = i[f'Set{str(j)}_A']
                setpointb = i[f'Set{str(j)}_B']
                if setpointa == '-' or setpointb == '-':
                    break
                if int(setpointb) > int(setpointa):
                    B_won+=1
                B_played+=1

    if A_played == 0 and B_played == 0:
        print('There is no record of these teams so,50% winning chances for each.')
        return
    elif A_played == 0:
        A_win_rate = 0
        try:
            B_win_rate = (B_won/B_played) * 100
        except ZeroDivisionError:
            B_win_rate = 0
        print(f'There is no record of team A ({A_id}) but team B`s winning rate is {"{:.2f}".format(B_win_rate)}%')

    elif B_played == 0:
        A_win_rate = (A_won/A_played) * 100
        B_win_rate = 0
        print(f'There is no record of team B ({B_id}) but team A`s winning rate is {"{:.2f}".format(A_win_rate)}%')
        return
    else:
        A_win_rate = (A_won/A_played) * 100
        B_win_rate = (B_won/B_played) * 100

        probability_A = (A_win_rate / (A_win_rate + B_win_rate)) * 100
        probability_B = (B_win_rate / (A_win_rate + B_win_rate)) * 100

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
