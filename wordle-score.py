import re

scores = {
}

games_played = {
}

for line in open('chat.txt'):
    match = re.match(r'.*\- (.*): Wordle [0-9]+ ([1-6])\/6', line)
    if match:
        player = match.group(1)
        score = int(match.group(2))
        if player not in scores:
            scores[player] = 0
            games_played[player] = 0
        scores[player] += score
        games_played[player] += 1

for player in scores:
    print(f'{player}: average {scores[player] / games_played[player]:.02f} over {games_played[player]} games')