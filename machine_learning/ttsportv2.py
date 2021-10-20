import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import date, timedelta

# desktop_path = 'D:/klw/desktop/bettings/score/output_0826.xlsx'
desktop_path = 'output.xlsx'

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


def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None, truncate_sheet=False, **to_excel_kwargs):
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')
    if not os.path.exists(filename):
        df.to_excel(filename, **to_excel_kwargs)
        return

    df_dict = pd.read_excel(filename, sheet_name=sheet_name)
    df = pd.concat([df_dict, df])
    df.to_excel(filename, **to_excel_kwargs)


while True:
    date1 = input('Enter start date or date yyyy-mm-dd as 2021-08-11 : ').split('-')
    date2 = input('Enter end date or date yyyy-mm-dd as 2021-08-11 : ').split('-')

    rang = input('Enter group to look for :')

    sdate = date(int(date1[0]), int(date1[1]), int(date1[2]))  # start date
    edate = date(int(date2[0]), int(date2[1]), int(date2[2]))  # end date

    delta = edate - sdate

    for i in range(delta.days + 1):
        date = sdate + timedelta(days=i)
        date = str(date).split('-')
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

            try:
                groups_dict[no] = {'group': tournament[1], 'url': url, 'rank': no}
                print(no, ' '.join(tournament))
            except IndexError:
                pass
        tournament = rang

        for info in groups_dict:
            if groups_dict[info]['group'] == tournament:
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
                    temp_row.insert(0, '-'.join(date))
                    rows.append(temp_row)

                df1 = pd.DataFrame(rows)
                append_df_to_excel(desktop_path, df1, index=None)
                print('\n\n')
                print(df1.to_string())

        groups_dict = {}
