from google.cloud import datastore
import json

out_file = open('player_table.csv', 'w+')


def write_file(row):
    tmp = []
    for ch in row:
        tmp.append(str(ch))
    out_file.write(','.join(tmp))
    out_file.write('\n')


def generate_player_statistics():
    client = datastore.Client()
    event_kind = 'Player_Statistic_Data'
    query = client.query(kind=event_kind)
    offset = 0
    while True:
        all_players = list(query.fetch(limit=100, offset=offset))
        generate_statistics(all_players)
        offset = offset + 100
        print("fetched data", offset)
        if len(all_players) == 0:
            break


def generate_statistics(all_players: list):
    header = ['playerID', 'win_rate', 'average_max_points_in_a_row', 'average_service_points_lost',
              'average_biggest_lead', 'average_receiver_points_won', 'average_service_points_won',
              'average_service_error', 'average_comeback_loss', 'average_comeback_to_win',
              'average_receiver_points_lost', 'average_points']

    write_file(header)

    for player in all_players:
        row = []
        name = player.key
        name = str(name)[30:]
        name = name[:name.find(')')]
        row.append(name)
        player = json.loads(json.dumps(player), parse_int=str)

        required_data = player['all_matches']['overall']

        for data in header[1:]:
            row.append(required_data[data])
        write_file(row)
        row.clear()


if __name__ == '__main__':
    generate_player_statistics()
