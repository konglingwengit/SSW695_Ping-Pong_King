import json
import os

import requests
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

def get_career(teamid, counter=0):
    url = 'https://api.sofascore.com/api/v1/team/' + str(teamid) + '/events/last/' + str(counter)
    r = requests.Session()
    resp = r.get(url, headers=head).text
    # print(resp)
    if '"code":404' in str(resp):
        print('user not found')
        return 'false'
    return json.loads(resp)

def compute_status(teamid):
    resp = get_career(teamid)
    events = 0
    won = 0
    if resp == False:
        events = 'Nan'
        won = 'Nan'
        status = "Nan"
        return {"Played": events, "Won": won, "lose": 'Nan', "Status_points": status}
    for i in resp["events"][:10]:
        events += 1
        win = i['winnerCode']
        if i['homeTeam']['id'] == teamid:
            teamcode = 1
        elif i['awayTeam']['id'] == teamid:
            teamcode = 2
        else:
            teamcode = -1
            events -= 1
        if win == teamcode:
            won += 1

    status = won/10
    return {"Played": events, "Won": won, "lose": events-won, "Status_points": status}


def main_url():
    try:
        with open("ids.json", 'r') as f:
            ids = json.load(f)
    except:
        input("ids.json file not found.")

    stats = {}
    for i in ids.values():
        if i['homeTeamId'] not in stats.keys():
            print("loading ids")
            stats[i['homeTeamId']] = compute_status(i['homeTeamId'])
        if i['awayTeamId'] not in stats.keys():
            print("loading ids")
            stats[i['awayTeamId']] = compute_status(i['awayTeamId'])

    with open("statistics/teams.json", 'w') as f:
        json.dump(stats, f)


def main_file():
    files = len([name for name in os.listdir('./events')])

    players = {}
    for i in range(1, files+1):
        s = f'events/{i}.json'
        with open(s, 'r') as f:
            j = json.load(f)

        for i in j['events']:
            a = i['homeTeam']['id']
            b = i['awayTeam']['id']
            won = i['winnerCode']
            if won == 1:
                if a in players.keys():
                    players[a] = {'Played': players[a]['Played']+1, 'Won': players[a]['Won']+1, 'Lose':players[a]['Lose']}
                else:
                    players[a] = {'Played': 1, 'Won':1, 'Lose':0}
                if b in players.keys():
                    players[b] = {'Played': players[b]['Played'] + 1, 'Won': players[b]['Won'],
                                  'Lose': players[b]['Lose']+1}
                else:
                    players[b] = {'Played': 1, 'Won':0, 'Lose':1}
            if won == 2:
                if a in players.keys():
                    players[a] = {'Played': players[a]['Played']+1, 'Won': players[a]['Won'], 'Lose':players[a]['Lose']+1}
                else:
                    players[a] = {'Played': 1, 'Won':0, 'Lose':1}
                if b in players.keys():
                    players[b] = {'Played': players[b]['Played'] + 1, 'Won': players[b]['Won']+1,
                                  'Lose': players[b]['Lose']}
                else:
                    players[b] = {'Played': 1, 'Won':1, 'Lose':0}
    for i in players.values():
        status = (i['Won']/i['Played'])*100
        i['Status_points'] = status

    with open("statistics/teams.json", 'w') as f:
        json.dump(players, f)

def all_for_one_file(id):
    files = len([name for name in os.listdir('./events')])
    print(files)
    players = {}
    for i in range(1, files+1):
        s = f'events/{i}.json'
        with open(s, 'r') as f:
            j = json.load(f)

        for i in j['events']:
            a = i['homeTeam']['id']
            b = i['awayTeam']['id']
            if a == id:
                print(a)
            if b == id:
                print(b)
            won = i['winnerCode']
            if won == 1:
                if a in players.keys():
                    players[a] = {'Played': players[a]['Played']+1, 'Won': players[a]['Won']+1, 'Lose':players[a]['Lose']}
                else:
                    players[a] = {'Played': 1, 'Won':1, 'Lose':0}
                if b in players.keys():
                    players[b] = {'Played': players[b]['Played'] + 1, 'Won': players[b]['Won'],
                                  'Lose': players[b]['Lose']+1}
                else:
                    players[b] = {'Played': 1, 'Won':0, 'Lose':1}
            if won == 2:
                if a in players.keys():
                    players[a] = {'Played': players[a]['Played']+1, 'Won': players[a]['Won'], 'Lose':players[a]['Lose']+1}
                else:
                    players[a] = {'Played': 1, 'Won':0, 'Lose':1}
                if b in players.keys():
                    players[b] = {'Played': players[b]['Played'] + 1, 'Won': players[b]['Won']+1,
                                  'Lose': players[b]['Lose']}
                else:
                    players[b] = {'Played': 1, 'Won':1, 'Lose':0}
    for i in players.values():
        status = (i['Won']/i['Played'])*100
        i['Status_points'] = status
    print(players[id])
    # with open("statistics/teams.json", 'w') as f:
    #     json.dump(players, f)

def all_for_one_url(id):
    i = 0
    l = []
    teamid = id
    while i == 0:
        print('fetching')
        x = get_career(teamid, i)
        i+=1
        if x == 'false':
            break
        l.append(x)

    events = 0
    won = 0
    for resp in l:
        for i in resp["events"]:
            events += 1
            win = i['winnerCode']
            if i['homeTeam']['id'] == teamid:
                teamcode = 1
            elif i['awayTeam']['id'] == teamid:
                teamcode = 2
            else:
                teamcode = -1
                events -= 1
            if win == teamcode:
                won += 1

    status = (won / events) * 100
    print({"Played": events, "Won": won, "lose": events - won, "Status_points": status})

if __name__ == '__main__':
    # id = 345139
    # all_for_one_url(id)
    # all_for_one_file(id)
    main_url()
