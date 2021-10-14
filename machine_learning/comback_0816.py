#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
from time import sleep
from datetime import datetime
import copy
import collections
import matplotlib.pyplot as plt

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
        url = 'https://www.sofascore.com/team/' + each_player['sport']['slug'] + '/' + each_player['slug'] + '/' + str(
            each_player['id'])
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

    counter = collections.Counter(come_back_player['comebackA'])
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
    counter = collections.Counter(come_back_match['comebackA'])
    keysA = counter.keys()
    valuesA = counter.values()
    print(come_back_match["shortNameA"][0])
    plt.bar(keysA, valuesA)
    plt.show()

    counter = collections.Counter(come_back_match['comebackB'])
    keysB = counter.keys()
    valuesB = counter.values()
    print(come_back_match["shortNameB"][0])
    plt.bar(keysB, valuesB)
    plt.show()

    return come_back_match


max_check, come_back = '', ''


def start_comeback():
    global max_check, come_back
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
            return
