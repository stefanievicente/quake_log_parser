import re
import json
import itertools

kill = re.compile(r'.*Kill:.*:(.*)killed(.*)by', re.IGNORECASE)
name_change = re.compile(r'.*ClientUserinfoChanged:(.*)n\\(.*)\\t\\0.*', re.IGNORECASE)

total_kills = 0
players = {}
num_game = 0

with open("Quake.txt", "rt", encoding="utf-8") as file:
    content = file.read()

splitting_games = content.split('InitGame')
splitting_games = splitting_games[1:]

for item in splitting_games:

    num_game +=1
    
    prev_num, prev_name = '', ''
    num, name = '', ''
    name_dict = {}

    lines = item.split('\n')

    for line in lines:

        if kill.match(line):
            total_kills +=1
            death = kill.match(line)
            killer = death.group(1).strip()
            dead = death.group(2).strip()
            if killer != '<world>' and killer not in players.keys():
                players[killer] = 1 
            elif killer in players.keys():
                players[killer] = players[killer] + 1 
            if dead.strip() not in players.keys():
                players[dead] = 0
            if killer == '<world>':
                players[dead] = players[dead] - 1 

        if name_change.match(line):
            change = name_change.match(line)
            prev_num, prev_name = num, name
            num = change.group(1).strip()
            name = change.group(2).strip()
            if prev_num == num:
                if prev_name != name:
                    name_dict[name] = prev_name
                else:
                    if name not in players.keys():
                        players[name] = 0
            
    id = list(players.keys())

    answer = []

    for player in players:
        answer.append({
            'id': id.index(player) + 1,
            'name': player,
            'kills': int(players[player]), 
            'old_names': []
        })

    for player in answer:
        for name in name_dict:
            if player['name'] == name:
                player['old_names'] = name_dict[name]

    for a, b in itertools.combinations(answer, 2):
        if a['old_names'] == b['name']:
            a['kills'] = a['kills'] + b['kills']
            b['kills'] = 0
            answer.remove(b)

    game = {'game': num_game,
         'status': {
             'total_kills': total_kills,
             'players': []
          }
        }

    for player in answer:
        game['status']['players'].append(player)
    
    with open("parsed.txt", "a", encoding="utf-8") as answer:
        answer.write(json.dumps(game, indent=2))

    total_kills = 0
    players = {}