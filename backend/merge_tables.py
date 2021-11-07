players_dict = {}
with open('player_table.csv', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n', '').split(',')
        players_dict[line[0]] = line

p1 = []
p2 = []
for p in players_dict['playerID']:
    p1.append(f'playerA_' + p)
    p2.append(f'playerB_' + p)
players_dict['player_data'] = p1[1:] + p2[1:]

print(players_dict['player_data'])

with open('final_table.csv', 'w+') as out:
    with open('game_table.csv', 'r') as f:
        for c, line in enumerate(f.readlines()):
            line = line.replace('\n', '').split(',')
            if c == 0:
                out.write(','.join(line + players_dict['player_data']) + '\n')
                continue
            line = line + players_dict[line[0]][1:]
            line = line + players_dict[line[1]][1:]

            out.write(','.join(line)+'\n')
