import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from google.cloud import datastore

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


client = None


def add_to_db(csv_row):
    global client
    if client is None:
        client = datastore.Client()
    entity = datastore.entity.Entity()
    entity.key = client.key('RawCSV_Match')
    entity['date'] = csv_row[0]
    entity['tournament_time_index'] = csv_row[1]
    entity['game_start_time'] = csv_row[2]
    entity['first_player'] = csv_row[3]
    entity['first_player_rank_data'] = csv_row[4]
    entity['scoring_data'] = csv_row[5]
    entity['unknown1'] = csv_row[6]
    entity['match_points'] = csv_row[7]
    entity['unknown2'] = csv_row[8]
    entity['second_player_rank_data'] = csv_row[9]
    entity['second_player'] = csv_row[10]
    entity['unknown3'] = csv_row[11]
    query = client.query(kind='RawCSV_Match')
    query.add_filter('date', '=', csv_row[0])
    query.add_filter('game_start_time', '=', csv_row[2])
    query.add_filter('first_player', '=', csv_row[3])
    query.add_filter('second_player', '=', csv_row[10])
    query_result = list(query.fetch())
    if len(query_result) == 0:
        client.put(entity)


def scrape_data(start_date: str, end_date: str, rank_range: str):
    start_date = start_date.split('-')
    end_date = end_date.split('-')
    sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))  # start date
    edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))  # end date

    delta = edate - sdate

    for i in range(delta.days + 1):
        target_date = sdate + timedelta(days=i)
        target_date = str(target_date).split('-')
        if [''] == target_date:
            exit()

        resp = requests.get(f'https://tt.sport-liga.pro/tours/?year={target_date[0]}&month={target_date[1]}&day={target_date[2]}',
                            headers=header).text
        site_url = 'https://tt.sport-liga.pro/'

        soup = BeautifulSoup(resp, 'html.parser')

        names = soup.findAll('td', {'class': 'tournament-name'})
        groups_dict = {}

        for no, name in enumerate(names):
            url = site_url + name.find('a').get('href')
            tournament = name.find('a').text
            tournament = str(tournament).replace(' ', '').split('\n')[0].split('.league')

            try:
                groups_dict[no] = {'group': tournament[1], 'url': url, 'rank': no}
                print(no, ' '.join(tournament))
            except IndexError:
                pass

        for info in groups_dict:
            if groups_dict[info]['group'] == rank_range or rank_range is None:
                get_url = groups_dict[info]['url']
                resp = requests.get(get_url, headers=header).text
                soup = BeautifulSoup(resp, 'html.parser')
                table = soup.find('table', {'class': 'games_list'})
                # print(table)
                rows = []
                tr_row = table.findAll('tr')[1:]

                for count, row in enumerate(tr_row):
                    single = row.findAll('td')
                    if len(single) == 3:
                        continue
                    temp_row = []
                    for data in single:
                        data = str(data.text).replace('\n', '')
                        temp_row.append(data)
                    temp_row.insert(0, groups_dict[info]['rank'])
                    temp_row.insert(0, '-'.join(target_date))
                    add_to_db(temp_row)


def add_player(name: str):
    entity = datastore.entity.Entity()
    entity.key = client.key('Player')
    entity['name'] = name
    client.put(entity)


def update_player_list():
    global client
    if client is None:
        client = datastore.Client()
    query = client.query(kind='RawCSV_Match')
    query_iter = query.fetch()
    for match in query_iter:
        player_query = client.query(kind='Player')
        player_query.add_filter('name', '=', match['first_player'])
        player_list = list(player_query.fetch())
        if len(player_list) == 0:
            add_player(match['first_player'])
        player_query = client.query(kind='Player')
        player_query.add_filter('name', '=', match['second_player'])
        player_list = list(player_query.fetch())
        if len(player_list) == 0:
            add_player(match['second_player'])
