import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import json
from time import sleep
from datetime import datetime
import copy
import collections
import matplotlib.pyplot as plt
from pathlib import Path
import sklearn


desktop_path = '/Users/lingwenkong/Desktop/ping-pong-king/data/output.xlsx'

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0',
    'cookie': 'PHPSESSID=9ba1f08a925af17edf4431998ee7206e; _ga=GA1.1.221324312.1629782069; '
              '_ym_uid=1629782069273124061; _ym_d=1629782069; _ym_isad=2; googtrans=/ru/en; googtrans=/ru/en; '
              'lang=en; _ga_JYTDEKEFDJ=GS1.1.1629782068.1.1.1629782170.0',
    'if-modified-since': 'Tue, 24 Aug 2021 05:16:07 GMT',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36'}


def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False,
                       **to_excel_kwargs):
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')
    if not os.path.exists(filename):
        df.to_excel(filename, **to_excel_kwargs)
        return

    df_dict = pd.read_excel(filename, sheet_name=sheet_name)
    df = pd.concat([ df_dict,df])
    df.to_excel(filename, **to_excel_kwargs)


while True:
    date = input('press Enter to exit or date yyyy-mm-dd as 2021-08-11 : ').split('-')
    # date = '2021-08-11'.split('-')
    if [''] == date:
        exit()
    # date = '2021-08-11'.split('-')
    resp = requests.get(f'https://tt.sport-liga.pro/tours/?year={date[0]}&month={date[1]}&day={date[2]}',
                        headers=header).text
    site_url = 'https://tt.sport-liga.pro/'

    soup = BeautifulSoup(resp, 'html.parser')

    names = soup.findAll('td', {'class': 'tournament-name'})
    groups_dict = {}

    for no, name in enumerate(names):
        url = site_url + name.find('a').get('href')
        tournament = name.find('a').text
        tournament = str(tournament).replace(' ', '').split('\n')[0].split('.league')
        print(no ,' '.join(tournament))
        groups_dict[no] = {'group': tournament[1], 'url': url, 'rank': no}
    tournament = input('Please input group of tournament:')
    # tournament = '400-450'

    for info in groups_dict:
        if groups_dict[info]['group'] == tournament:
            get_url = groups_dict[info]['url']
            resp = requests.get(get_url, headers = header).text
            soup = BeautifulSoup(resp, 'html.parser')
            table = soup.find('table', {'class': 'games_list'})
            # print(table)
            rows = []
            for count, row in enumerate(table.findAll('tr')[1:]):
                single = row.findAll('td')
                if len(single) == 3:
                    continue
                temp_row = []
                for data in single:
                    data = str(data.text).replace('\n', '')
                    temp_row.append(data)
                temp_row.insert(0,groups_dict[info]['rank'])
                temp_row.insert(0,'-'.join(date))
                rows.append(temp_row)

            df1 = pd.DataFrame(rows)
            append_df_to_excel(desktop_path, df1, index=None)
            print('\n\n')
            print(df1.to_string())

    groups_dict = {}

head = {
    'Host': 'api.sofascore.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://www.sofascore.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
}


def get_url_by_name(name='Gusev V.'):
    name = name.replace(' ', '%20')
    search_result = requests.get('https://api.sofascore.com/api/v1/search/teams/' + name, headers=head).text

    # print(search_result)
    search_result = json.loads(search_result)

    urls = []
    for each_player in search_result['teams']:
        url = 'https://www.sofascore.com/team/' + each_player['sport']['slug'] + '/' + each_player['slug'] + '/' +               str(each_player['id'])
        urls.append([url, str(each_player['id']), each_player['slug']])
        print(url)
    try:
        return urls[0]
    except IndexError:
        print('Name not found ')
        exit()


def get_event_ids(search_result, slug):
    search_result = json.loads(search_result)
    # print(search_result)
    comebacks = {'comebackA': [],
                 'comebackB': [],
                 'shortNameA': [],
                 'shortNameB': []

                 }
    shortName = slug
    url = 'https://api.sofascore.com/api/v1/event/'
    for count, each_game in enumerate(search_result['events']):
        # print(each_game)
        # dt = datetime.fromtimestamp(each_game['time']['currentPeriodStartTimestamp'])
        # sleep(2)
        if count > max_check: break
        try:
            event_id = each_game['id']
            if event_id == '':
                continue
        except KeyError:
            continue
        resp = requests.get(url + str(event_id) + '/statistics', headers=head)
        map_event = json.loads(resp.text)

        try:
            home = 0
            away = 0
            if each_game['homeTeam']['slug'] == shortName:
                # shortName1 = each_game['awayTeam']['slug']
                name2 = each_game['awayTeam']['shortName']
                name1 = each_game['homeTeam']['shortName']
                home = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['home']
                away = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['away']

            elif each_game['awayTeam']['slug'] == shortName:
                # shortName1 = each_game['homeTeam']['shortName']
                name1 = each_game['awayTeam']['shortName']
                name2 = each_game['homeTeam']['shortName']
                away = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['home']
                home = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['away']

            comebacks['comebackA'].append(int(home))
            comebacks['shortNameA'].append(name1)

            comebacks['comebackB'].append(int(away))
            comebacks['shortNameB'].append(name2)

        except KeyError:
            pass
    return comebacks


def get_match_ids(search_result):
    search_result = json.loads(search_result)
    # print(search_result)
    comebacks = {'comebackA': [],
                 'comebackB': [],
                 'shortNameA': [],
                 'shortNameB': []

                 }
    url = 'https://api.sofascore.com/api/v1/event/'
    shortName = search_result['events'][0]['homeTeam']['shortName']
    for count, each_game in enumerate(search_result['events']):
        # print(each_game)
        # dt = datetime.fromtimestamp(each_game['time']['currentPeriodStartTimestamp'])

        # sleep(2)
        if count > max_check: break
        try:
            event_id = each_game['id']
            if event_id == '':
                continue
        except KeyError:
            continue
        resp = requests.get(url + str(event_id) + '/statistics', headers=head)
        map_event = json.loads(resp.text)

        try:
            home = 0
            away = 0
            if each_game['homeTeam']['shortName'] == shortName:
                shortName1 = each_game['awayTeam']['shortName']
                home = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['home']
                away = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['away']

            elif each_game['awayTeam']['shortName'] == shortName:
                shortName1 = each_game['homeTeam']['shortName']
                away = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['home']
                home = map_event['statistics'][0]['groups'][0]['statisticsItems'][2]['away']

            comebacks['comebackA'].append(int(home))
            comebacks['shortNameA'].append(shortName)

            comebacks['comebackB'].append(int(away))
            comebacks['shortNameB'].append(shortName1)

        except KeyError:
            pass
    return comebacks


def get_career(teamid=345350, counter=0):
    url = 'https://api.sofascore.com/api/v1/team/' + str(teamid) + '/events/last/' + str(counter)
    r = requests.Session()
    resp = r.get(url, headers=head).text
    # print(resp)
    if '"code":404' in str(resp):
        print('user not found')
        return 'false'
    return resp


def get_h2h(match_url):
    match_obj = str(match_url).replace('https://www.sofascore.com/', '')
    match_id = match_obj.split('/')[1]
    url = 'https://api.sofascore.com/api/v1/event/' + str(match_id) + '/h2h/events'
    r = requests.Session()
    resp = r.get(url, headers=head).text
    if '"code":404' in str(resp):
        print('match not found')
        exit()
    return resp


def print_info(nameA=None, url=None, match_url=None):
    if not url:
        info = get_url_by_name(nameA)
        team_id = info[1]
        slug = info[2]
    else:
        url = str(url).replace('https://www.sofascore.com/team/table-tennis/', '')
        url = url.split('/')
        slug = url[0]
        team_id = url[1].replace('/', '')
    if url is None and nameA is None:
        return
    first = True
    come_back_A = []
    come_back_B = []
    for counter in range(int(max_check / 29)):
        result = get_career(team_id, counter)
        if result == 'false':
            print('player career matches already scraped.')
            break
        temp = get_event_ids(result, slug)
        if first:
            come_back_A = temp['comebackA']
            come_back_B = temp['comebackB']
            come_back_player = copy.deepcopy(temp)
            first = False
            continue
        come_back_A = come_back_A + temp['comebackA']
        come_back_B = come_back_B + temp['comebackB']

    come_back_player['comebackA'] = come_back_A
    come_back_player['comebackB'] = come_back_B
    print(come_back_player['shortNameA'][0], 'max comeback: ', ':', max(come_back_player['comebackA']))

    print('opponents', ' max comeback: ', max(come_back_player['comebackB']))

    print(come_back_player['shortNameA'], 'Max comeback: ', come_back_player['comebackA'])
    
    print(come_back_player['shortNameB'], 'opponents', 'Max comeback: ', ':', come_back_player['comebackB'])
    
    counter=collections.Counter(come_back_player['comebackA'])
    keysA = counter.keys()
    valuesA = counter.values()
    print(come_back_player["shortNameA"][0])
    plt.bar(keysA, valuesA)
    plt.show()

    return come_back_player


def print_match(match_url):
    result = get_h2h(match_url)

    come_back_match = get_match_ids(result)

    print(come_back_match['shortNameA'][0], 'Max comeback: ', ':', max(come_back_match['comebackA']))

    print(come_back_match['shortNameB'][0], 'Max comeback: ', ':', max(come_back_match['comebackB']))

    print(come_back_match['shortNameA'][0], ' comebacks: ', ':', come_back_match['comebackA'])

    print(come_back_match['shortNameB'][0], ' comebacks: ', ':', come_back_match['comebackB'])
    counter=collections.Counter(come_back_match['comebackA'])
    keysA = counter.keys()
    valuesA = counter.values()
    print(come_back_match["shortNameA"][0])
    plt.bar(keysA, valuesA)
    plt.show()

    counter=collections.Counter(come_back_match['comebackB'])
    keysB = counter.keys()
    valuesB = counter.values()
    print(come_back_match["shortNameB"][0])
    plt.bar(keysB, valuesB)
    plt.show()
    

    return come_back_match


if __name__ == '__main__':

    max_check = int(input('Enter Value for number of matches to view against player:'))

    while True:
        mode = input('\nPress 1 for player mode\nPress 2 for match mode  \nPress 0 for exit \nEnter choice :')
        # https://www.sofascore.com/kulikov-nemashkalo/yzMcsByVc
        mode = int(mode)
        if mode == 2:
            match_url = input('input match url:')
            print_match(match_url)
        if mode == 1:

            nameA = input('Input player 1 url like this or his name\n'
                          'Enter URL: ')
            print('\n')
            if 'http' in nameA:
                come_back = print_info(url=nameA)
            else:
                come_back = print_info(nameA=nameA)
        if mode not in [1, 2]:
            exit()

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
        if(r.status_code == 403):
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

def fetch_statistics(game_id, time , a_id, b_id, a_name, b_name):

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
            groups = i['groups']
            a_points.append(groups[0]['statisticsItems'][0]['home'])
            b_points.append(groups[0]['statisticsItems'][0]['away'])
            a_max_in_row.append(int(groups[2]['statisticsItems'][3]['home']))
            b_max_in_row.append(int(groups[2]['statisticsItems'][3]['away']))
            rounds += 1
    except:
        a_max_in_row = [0]
        b_max_in_row = [0]
    for j in range(5-rounds):
        a_points.append("-")
        b_points.append("-")
    a_max_in_row = sum(a_max_in_row) / len(a_max_in_row)
    b_max_in_row = sum(b_max_in_row) / len(b_max_in_row)

    obj = {"Date": str(timestamp.date()), "Time": str(timestamp.time()),
           "Player_A_ID": a_id, "Player_B_ID": b_id,
           "Player_A_Name": a_name, "Player_B_Name": b_name,
           "Set1_A": a_points[0], "Set1_B": b_points[0],
           "Set2_A": a_points[1], "Set2_B": b_points[1],
           "Set3_A": a_points[2], "Set3_B": b_points[2],
           "Set4_A": a_points[3], "Set4_B": b_points[3],
           "Set5_A": a_points[4], "Set5_B": b_points[4],
           "PlayerA's Avg Max Points In a Row": a_max_in_row,
           "PlayerB's Avg Max Points In a Row": b_max_in_row,
           "A`s Status Points": a_status_point,
           "B`s Status Points": b_status_point,
           }
    return obj

def create_excel():
    data_arr = []
    with open('ids.json', 'r') as file:
        data = json.load(file)
    for i in data.keys():
        x = fetch_statistics(data[i]["GameId"], data[i]["startTimestamp"], data[i]["homeTeamId"], data[i]["awayTeamId"],data[i]["homeTeamName"], data[i]["awayTeamName"])
        data_arr.append(x)
    dateframe = pd.DataFrame(data_arr)
    dateframe.to_excel('report.xlsx')

def fetch_ids_from_file():
    ids = {}
    files = len([name for name in os.listdir('./events')])
    if files == 0:
        fetch_ids()
        return
    for i in range(1, files+1):
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


if __name__ == "__main__":

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
