import os
import time
import datetime
import requests
import json
from google.cloud import datastore

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

client = None


def fetch_tournament(tournament_id):
    global client
    if client is None:
        client = datastore.Client()
    event_kind = 'Event_Data'
    player_kind = 'Player'
    i = 0
    while True:
        print('Event request')
        r = requests.get(f'https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/events/last/{i}', headers=head)
        i += 1
        print(f'starting iteration {i}')
        if r.status_code == 403:
            print('Error 403 occurred while fetching data ( IP Blocked) try VPN')
        if r.status_code == 200:
            raw_data = json.loads(r.text)
            for d in raw_data['events']:
                new_event = datastore.entity.Entity()
                event_id = int(d['id'])
                new_event.key = client.key(event_kind, event_id)

                found = client.get(new_event.key)

                #  Don't make another copy of an event we already recorded.
                if found is None:
                    new_event['timestamp'] = d['startTimestamp']
                    new_event['uniqueTournament'] = d['tournament']['uniqueTournament']['id']
                    new_event['sport'] = d['tournament']['category']['sport']
                    new_event['homeTeam'] = d['homeTeam']['id']
                    new_event['awayTeam'] = d['awayTeam']['id']
                    new_event['homeScore'] = d['homeScore']
                    new_event['awayScore'] = d['awayScore']
                    new_event['winnerCode'] = d['winnerCode']

                    req_stat = requests.get(f'https://api.sofascore.com/api/v1/event/{event_id}/statistics',
                                            headers=head)
                    if req_stat.status_code == 200:
                        stat = json.loads(req_stat.text)
                        for period in range(len(stat['statistics'])):
                            statistic = dict()
                            current_statistic = stat['statistics'][period]['groups'][0]['statisticsItems']
                            for statistic_id in range(len(current_statistic)):
                                statistic[current_statistic[statistic_id]['name']] = \
                                    {'home': current_statistic[statistic_id]['home'],
                                     'away': current_statistic[statistic_id]['away']}
                            if period == 0:
                                new_event['overall_statistics'] = statistic
                            else:
                                new_event[f'statistics_period{period}'] = statistic

                    # This appears to be the code for completed games
                    if d['status']['code'] == 100:
                        client.put(new_event)
                    new_player = datastore.entity.Entity()
                    new_player.key = client.key(player_kind, int(d['homeTeam']['id']))
                    found = client.get(new_player.key)
                    if found is None:
                        new_player['name'] = d['homeTeam']['name']
                        client.put(new_player)
                    new_player = datastore.entity.Entity()
                    new_player.key = client.key(player_kind, int(d['awayTeam']['id']))
                    found = client.get(new_player.key)
                    if found is None:
                        new_player['name'] = d['awayTeam']['name']
                        client.put(new_player)
            if not raw_data['hasNextPage']:
                break
            time.sleep(5)
        else:
            break


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


if __name__ == '__main__':
    fetch_tournament(15001)
