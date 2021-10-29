import os
import time
import datetime
import requests
import json
import pandas as pd
from pathlib import Path

head = {
    'Host': 'api.sofascore.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://www.sofascore.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
}


def check_new_ids():
    with open('ids.json', 'r') as file:
        ids = json.load(file)
        counter = 0
    for i in range(100):
        r = requests.get(f'https://api.sofascore.com/api/v1/unique-tournament/14770/events/last/{i}', headers=head)
        if r.status_code != 200:
            break
        new = json.loads(r.text)
        with open(f'events/1.json', 'r') as filx:
            fx = json.load(filx)

        for i in new['events']:
            if str(i['id']) not in ids.keys():
                fx['events'].append(i)
                print("added new entry id: ", i['id'])
                game_id = i['id']
                timestamp = i['startTimestamp']
                a_id = i['homeTeam']['id']
                b_id = i['awayTeam']['id']
                a_name = i['homeTeam']['name']
                b_name = i['awayTeam']['name']
                obj = {"GameId": game_id, "startTimestamp": timestamp,
                       "homeTeamId": a_id, "awayTeamId": b_id,
                       "homeTeamName": a_name, "awayTeamName": b_name
                       }
                ids[game_id] = obj
                counter += 1
        if counter <= 25:
            break
    with open('ids.json', 'w') as file:
        json.dump(ids, file)
    with open(f'events/1.json', 'w') as filx:
        json.dump(fx, filx)


def fetch_ids():
    ids = {}
    i = 0
    while True:
        r = requests.get(f'https://api.sofascore.com/api/v1/unique-tournament/14770/events/last/{i}', headers=head)
        i += 1
        if (r.status_code == 403):
            print('Error 403 occured while fetching data ( IP Blocked) try VPN')
        if r.status_code == 200:
            raw_data = json.loads(r.text)
            s = f'events/{i}.json'
            with open(s, 'w') as outfile:
                json.dump(raw_data, outfile)
            for d in raw_data['events']:
                game_id = d['id']
                timestamp = d['startTimestamp']
                a_id = d['homeTeam']['id']
                b_id = d['awayTeam']['id']
                a_name = d['homeTeam']['name']
                b_name = d['awayTeam']['name']
                obj = {"GameId": game_id, "startTimestamp": timestamp,
                       "homeTeamId": a_id, "awayTeamId": b_id,
                       "homeTeamName": a_name, "awayTeamName": b_name
                       }
            time.sleep(5)
        else:
            break

    with open('ids.json', 'w') as outfile:
        json.dump(ids, outfile)


def fetch_statistics(game_id, time, a_id, b_id, a_name, b_name):
    timestamp = datetime.datetime.fromtimestamp(time)
    a_points = []
    b_points = []
    a_max_in_row = []
    b_max_in_row = []
    a_status_point = "Nan"
    b_status_point = "Nan"
    rounds = 0

    try:
        with open(f'statistics/teams.json', 'r') as f:
            j = json.load(f)
            a_status_point = j[str(a_id)]['Status_points']
            b_status_point = j[str(b_id)]['Status_points']
    except:
        pass

    try:
        with open(f'statistics/{game_id}.json', 'r') as f:
            j = json.load(f)
        print("record found from statistics dir...")
    except:
        print("record not found in statistics dir fetching from api")
        r = requests.get(f'https://api.sofascore.com/api/v1/event/{game_id}/statistics', headers=head)
        j = json.loads(r.text)
        # time.sleep(5)
        s = f'statistics/{game_id}.json'
        with open(s, 'w') as f:
            json.dump(j, f)

    try:
        for i in j['statistics']:
            # print(i)
            groups = i['groups']
            a_points.append(groups[0]['statisticsItems'][0]['home'])
            b_points.append(groups[0]['statisticsItems'][0]['away'])
            if rounds > 0:
                a_max_in_row.append(int(groups[2]['statisticsItems'][3]['home']))
                b_max_in_row.append(int(groups[2]['statisticsItems'][3]['away']))
            rounds += 1
    except:
        a_max_in_row = [0]
        b_max_in_row = [0]
    for j in range(5 - rounds):
        a_points.append("-")
        b_points.append("-")
    try:
        a_max_in_row = sum(a_max_in_row) / len(a_max_in_row)
        b_max_in_row = sum(b_max_in_row) / len(b_max_in_row)
    except ZeroDivisionError:
        a_max_in_row = 0
        b_max_in_row = 0
    try:
        print(str(a_points[0]), str(b_points[0]))
        if int(a_points[0]) > int(b_points[0]):
            who_won = a_id
        elif int(a_points[0]) < int(b_points[0]):
            who_won=b_id
        else:
            who_won = 0
    except ValueError:
        who_won = 0
    obj = {"Date": str(timestamp.date()), "Time": str(timestamp.time()),
           "Player_A_ID": a_id, "Player_B_ID": b_id,
           "Player_A_Name": a_name, "Player_B_Name": b_name,
           "total_match_points_A": a_points[0], "total_match_points_B": b_points[0],
           "Set2_A": a_points[1], "Set2_B": b_points[1],
           "Set3_A": a_points[2], "Set3_B": b_points[2],
           "Set4_A": a_points[3], "Set4_B": b_points[3],
           "Set5_A": a_points[4], "Set5_B": b_points[4],
           "PlayerA's Avg Max Points In a Row": a_max_in_row,
           "PlayerB's Avg Max Points In a Row": b_max_in_row,
           "A`s Status Points": a_status_point,
           "B`s Status Points": b_status_point,
           "who_won": who_won,
           }
    return obj


def create_excel():
    data_arr = []
    with open('ids.json', 'r') as file:
        data = json.load(file)
    for i in data.keys():
        x = fetch_statistics(data[i]["GameId"], data[i]["startTimestamp"], data[i]["homeTeamId"], data[i]["awayTeamId"],
                             data[i]["homeTeamName"], data[i]["awayTeamName"])
        data_arr.append(x)
    dateframe = pd.DataFrame(data_arr)
    dateframe.to_excel('report.xlsx')


def fetch_ids_from_file():
    ids = {}
    files = len([name for name in os.listdir('./events')])
    if files == 0:
        fetch_ids()
        return
    for i in range(1, files + 1):
        x = {}
        s = f'events/{i}.json'
        try:
            with open(s, 'r') as outfile:
                x = json.load(outfile)
            for d in x['events']:
                game_id = d['id']
                timestamp = d['startTimestamp']
                a_id = d['homeTeam']['id']
                b_id = d['awayTeam']['id']
                a_name = d['homeTeam']['name']
                b_name = d['awayTeam']['name']
                obj = {"GameId": game_id, "startTimestamp": timestamp,
                       "homeTeamId": a_id, "awayTeamId": b_id,
                       "homeTeamName": a_name, "awayTeamName": b_name
                       }
                ids[game_id] = obj
        except:
            pass

    with open('ids.json', 'w') as outfile:
        json.dump(ids, outfile)

    check_new_ids()


ids = {}


def start_tennis():
    global ids

    Path("./events").mkdir(parents=True, exist_ok=True)
    Path("./statistics").mkdir(parents=True, exist_ok=True)

    try:
        with open(f'statistics/Teams.json', 'r') as f:
            json.load(f)
    except:
        print("Status Points not found Try again after running Update_teams.py ")
        c = input('Or Press c to continue : ')
        if c not in ['c', 'C']:
            exit()
    try:
        with open('ids.json', 'r') as file:
            ids = json.load(file)
        fetch_ids_from_file()
    except:
        fetch_ids_from_file()
    create_excel()


if __name__ == '__main__':
    start_tennis()
