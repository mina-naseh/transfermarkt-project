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


def get_players_data(content, players_initial_data, season, club_id, players_club_history) -> None:
    players_selectors = content.select('table.items > tbody > tr')
    for player in players_selectors:
        compact_player_href = player.select_one('td.posrela td.hauptlink a').get("href")
        player_formatted_name = compact_player_href.rsplit('/')[1]
        player_id = compact_player_href.rsplit('/')[-1]
        player_foot = player.select_one('td:nth-child(7)').text
        player_market_value = player.select_one('td:nth-child(11)').text
        players_initial_data.append({"formatted_name": player_formatted_name, "id": player_id, "foot": player_foot})
        players_club_history.append({
            "player_id": player_id,
            "season": season,
            "club_id": club_id,
            "market_value": None if player_market_value == '-' else text_to_num( player_market_value.replace('\u20ac', '') )
        })


def crawl_players_list(base_url, headers, clubs_list, seasons):
    players_initial_data = []
    players_club_history = []
    for club in clubs_list:
        for season in seasons:
            club_players_url = f'{base_url}/{club["name"]}/kader/verein/{club["id"]}/plus/1/galerie/0?saison_id={season}'
            response = requests.get(club_players_url, headers=headers)
            content = BeautifulSoup(response.text, 'html.parser')
            get_players_data(content, players_initial_data, season, club["id"], players_club_history)
    with open("players_club_history.json", "w") as json_players_club_history_file:
        json.dump(players_club_history, json_players_club_history_file, indent=4)
