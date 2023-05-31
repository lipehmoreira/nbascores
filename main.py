# Query nba.live.endpoints.scoreboard and  list games in localTimeZone
import time
from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.live.nba.endpoints import playbyplay
from nba_api.stats.static import players
import os

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}"

# This block show all games in the current date
board = scoreboard.ScoreBoard()
print("ScoreBoardDate: " + board.score_board_date)
games = board.games.get_dict()
for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))

# Ask the user a game to track
live_game_id = input('Enter the ID of the game you wanna track: ')

while True:
    # Get the datasets
    box = boxscore.BoxScore(live_game_id)

    # I've removed part of this section | i'll be implemented soon
    pbp = playbyplay.PlayByPlay(live_game_id)
    line = "{action_number}: {period}:{clock} {player_id} ({action_type})"
    actions = pbp.get_dict()['game']['actions']  # plays are referred to in the live data as `actions`
    away = box.away_team.get_dict()
    home = box.home_team.get_dict()
    current_game = box.game.get_dict()

    # Start some variables to manipulate more easy
    home_name = home['teamName']
    home_score = home['score']
    away_name = away['teamName']
    away_score = away['score']

    # Clear the console
    os.system('cls')

    # Prints the live result
    print(f'{home_name} Vs. {away_name} | {current_game["gameStatusText"]}')
    print(f'{home_score} - {away_score}')
    #TODO Print the action (play by play)
    
    # Wait 1 sec then continue to exec
    #time.sleep(1)

    # Check if the game is over
    if current_game['gameStatusText'] == 'Final':
        print(f'{home_name} Vs. {away_name} | {current_game["gameStatusText"]}')
        print(f'{home_score} - {away_score}')
        os.system('pause')
        break
