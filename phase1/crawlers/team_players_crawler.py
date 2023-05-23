import json
import requests
from bs4 import BeautifulSoup


def text_to_num(text):
    d = {
        'k': 1000,
        'm': 1000000,
        'b': 1000000000
    }

    if text[-1] in d:
        # separate out the k, m, or b
        num, magnitude = text[:-1], text[-1]
        return int(float(num) * d[magnitude])
    else:
        return float(text)


def get_players_data(content, players_initial_data, unique_players_initial_data, season, team_id, players_team_history) -> None:
    players_selectors = content.select('table.items > tbody > tr')
    for player in players_selectors:
        compact_player_href = player.select_one('td.posrela td.hauptlink a').get("href")
        player_formatted_name = compact_player_href.rsplit('/')[1]
        player_id = compact_player_href.rsplit('/')[-1]
        player_foot = player.select_one('td:nth-child(7)').text
        player_market_value = player.select_one('td:nth-child(11)').text
        players_initial_data.append({
            "id": player_id,
            "formatted_name": player_formatted_name,
            "foot": player_foot,
            "season": season,
        })
        unique_player_info = {
            "id": player_id,
            "formatted_name": player_formatted_name,
        }
        if unique_player_info not in unique_players_initial_data:
            unique_players_initial_data.append(unique_player_info)
        players_team_history.append({
            "player_id": player_id,
            "season": season,
            "team_id": team_id,
            "market_value": None if player_market_value == '-' else text_to_num( player_market_value.replace('\u20ac', '') )
        })


def crawl_players_list(base_url, headers):
    unique_players_initial_data = []
    players_initial_data = []
    players_team_history = []
    with open('./crawlers/teams_data.json') as teams_json_file:
        teams = json.load(teams_json_file)
        for team in teams:
            print(f"team data is: {team}")
            team_players_url = f'{base_url}/{team["name"]}/kader/verein/{team["id"]}/plus/1/galerie/0?saison_id={team["year"]}'
            response = requests.get(team_players_url, headers=headers)
            content = BeautifulSoup(response.text, 'html.parser')
            get_players_data(content, players_initial_data, unique_players_initial_data, team["year"], team["id"], players_team_history)
    
    with open("unique_players_initial_data.json", "w") as json_unique_players_initial_data:
        json.dump(unique_players_initial_data, json_unique_players_initial_data, indent=4)
    
    with open("players_initial_data.json", "w") as json_players_initial_file:
        json.dump(players_initial_data, json_players_initial_file, indent=4)
    
    with open("players_team_history.json", "w") as json_players_team_history_file:
        json.dump(players_team_history, json_players_team_history_file, indent=4)
