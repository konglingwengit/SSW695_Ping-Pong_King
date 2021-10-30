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


def fetch_tournament(tournament_id, start_page, end_page):
    global client
    if client is None:
        client = datastore.Client()
    event_kind = 'Event_Data'
    player_kind = 'Player'
    i = start_page
    while i <= end_page:
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
