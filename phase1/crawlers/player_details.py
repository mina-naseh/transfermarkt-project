import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random
import time

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

required_leagues = ['2022 World Cup', 'UEFA Champions League', 'Premier League',
                    'World Cup 2018', 'Bundesliga', 'LaLiga', 'Serie A', 'Ligue 1']
leagues_id = {'2022 World Cup': 2022, 'UEFA Champions League': 500, 'Premier League': 501,
              'World Cup 2018': 2018, 'Bundesliga': 503, 'LaLiga': 502, 'Serie A': 504, 'Ligue 1': 505}
leagues_type = {"Premier League": 1, "Champions League": 2, "world Cup": 3}


leagues_df = pd.DataFrame(columns=['league_id', 'league_name', 'league_type'])
games_df = pd.DataFrame(
    columns=['game_id', 'date', 'home_team', 'away_team', 'result', 'matchday'])
players_df = pd.DataFrame(columns=['player_id', 'player_name',
                          'birthdate', 'height', 'main_position', 'national_team', 'foot'])
agent_df = pd.DataFrame(
    columns=['agent_id', 'agent_name', 'player_id', 'season'])
player_games_df = pd.DataFrame(columns=[
                               'player_id', 'team_id', 'game_id', 'player_position', 'sub_on', 'sub_off', 'played_minutes', 'bench', 'not_squad', 'injury'])
player_cards = pd.DataFrame(
    columns=['player_id', 'team_id', 'yellow_card', 'second_yellow_card', 'red_card'])
player_goals = pd.DataFrame(columns=['palyer_id', 'game_id', 'goals'])
player_assists = pd.DataFrame(columns=['palyer_id', 'game_id', 'assists'])
player_ownGoals = pd.DataFrame(columns=['palyer_id', 'game_id', 'own_goals'])

failed_links = pd.DataFrame(columns=['url'])


def extract_player_details(url, game_id, season, player_name, player_id, foot):
    headers = {
    'User-Agent': random.choice(user_agents),
    'Accept-Language': 'en-US,en;q=0.5'
    }
    global games_df, players_df, agent_df, player_games_df, player_cards, player_goals, player_assists, player_ownGoals
    global failed_links
    time.sleep(random.randint(2, 10))
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        li_tags = soup.find(
            'div', class_="data-header__info-box").find_all('li')
        birth = li_tags[0].find('span').text.strip()
        try:
            birthdate = datetime.strptime(
                birth, '%b %d, %Y (%M)').strftime('%Y-%m-%d')
        except:
            birthdate = datetime.strptime(
                birth, '%b %d, %Y').strftime('%Y-%m-%d')
        height, main_position, national_team, agent_name, agent_id = [None] * 5
        li_tags = soup.find(
            'div', class_="data-header__info-box").find_all('li')
        for a in range(len(li_tags)):
            info_type = li_tags[a]
            if "Position" in info_type.text.strip():
                main_position = info_type.find('span').text.strip()
            elif "Height" in info_type.text.strip():
                height = info_type.find('span').text.strip().replace(
                    "m", "").replace(",", "")
            elif "international" in info_type.text.strip() or "National" in info_type.text.strip() or "Former" in info_type.text.strip():
                national_team = info_type.find('span').text.strip()
            elif "Agent" in info_type.text.strip():
                agent_name = info_type.find('span').text.strip()
                agent_id = info_type.find('a')['href'].split('/')[4]

            box = soup.find_all('div', class_="box")
        for i in range(len(box)):
            league_div = box[i].find('div', class_="table-header")
            if league_div is None:
                continue
            league_name = league_div.find('a').text.strip()
            if league_name is None:
                continue
            try:
                player_team = soup.find('div', id="yw1").find('tbody').find_all(
                    'tr')[0].find_all('td')[2].find('a')['href'].split('/')[4]
            except:
                player_team = None
            if league_name in required_leagues:
                table = league_div.parent.find('tbody').find_all('tr')
                for t in range(len(table)):
                    td = table[t].find_all('td')
                    if len(td) > 4:
                        matchday = td[0].text.strip()
                        date = td[1].text
                        home_team = td[3].find('a')['title']
                        away_team = td[5].find('a')['title']
                        result = td[6].find('span').text.split(':')
                        # print(result)
                        none = [None] * 13
                        position, goals, assists, own_goals, yellow_cards, second_yellow_cards, red_cards, substitution_on, substitution_off, played_minutes, bench, injury, not_squad = none
                        if len(td) == 17:
                            position = td[7].find('a')['title']
                            # capitan = None if td[7].find('span') is None else td[7].find('span')['title']
                            goals = None if td[8].text == "" else td[8].text
                            assists = None if td[9].text == "" else td[9].text
                            own_goals = None if td[10].text == "" else td[10].text
                            yellow_cards = None if td[11].text == "" else td[11].text
                            second_yellow_cards = None if td[12].text == "" else td[12].text
                            red_cards = None if td[13].text == "" else td[13].text
                            substitution_on = None if td[14].text == "" else td[14].text
                            substitution_off = None if td[15].text == "" else td[15].text
                            played_minutes = None if td[16].text == "" else td[16].text.replace(
                                "'", "")
                        else:
                            status = td[7].text
                            if "bench" in status:
                                bench = td[7].text
                            elif status == "Not in squad":
                                not_squad = td[7].text
                            else:
                                injury = td[7].text
                    games_df = games_df._append({
                        'game_id': game_id,
                        'date': date,
                        'home_team': home_team,
                        'away_team': away_team,
                        'result': result,
                        'matchday': matchday
                    }, ignore_index=True)
                    player_games_df = player_games_df._append({
                        'player_id': player_id,
                        'team_id': player_team,
                        'game_id': game_id,
                        'player_position': position,
                        'sub_on': substitution_on,
                        'sub_off': substitution_off,
                        'played_minutes': played_minutes,
                        'bench': bench,
                        'not_squad': not_squad,
                        'injury': injury
                    }, ignore_index=True)
                    if red_cards != None or yellow_cards != None or second_yellow_cards != None:
                        player_cards = player_cards._append({
                            'player_id': player_id,
                            'team_id': player_team,
                            'yellow_card': yellow_cards,
                            'second_yellow_card': second_yellow_cards,
                            'red_card': red_cards
                        }, ignore_index=True)
                    if goals != None:
                        player_goals = player_goals._append({
                            'palyer_id': player_id,
                            'game_id': game_id,
                            'goals': goals
                        }, ignore_index=True)
                    if assists != None:
                        player_assists = player_assists._append({
                            'palyer_id': player_id,
                            'game_id': game_id,
                            'assists': assists
                        }, ignore_index=True)
                    if own_goals != None:
                        player_ownGoals = player_ownGoals._append({
                            'palyer_id': player_id,
                            'game_id': game_id,
                            'own_goals': own_goals
                        }, ignore_index=True)
        players_df = players_df._append({
            'player_id': player_id,
            'player_name': player_name,
            'birthdate': birthdate,
            'height': height,
            'main_position': main_position,
            'national_team': national_team,
            'foot': foot
        }, ignore_index=True)
        if agent_name != None:
            agent_df = agent_df._append({
                'agent_id': agent_id,
                'agent_name': agent_name,
                'player_id': player_id,
                'season': season
            }, ignore_index=True)

    except Exception as e:
        print(f"Error occurred for {url}: {e}")
        failed_links = failed_links._append({
            'url': url,
        }, ignore_index=True)


players_data = pd.read_json("players_initial_data.json")

for i in range(len(players_data)):
    id = players_data['id'][i]
    name = players_data['formatted_name'][i]
    season = players_data['season'][i]
    foot = players_data['foot'][i]
    url = f"https://www.transfermarkt.com/{name}/leistungsdatendetails/spieler/{id}/plus/1?saison={season}&verein=&liga=&wettbewerb=&pos=&trainer_id="
    print(i, name, season, url)
    extract_player_details(url=url, game_id=i, season=season,
                           player_name=name, player_id=id, foot=foot)
    games_df.to_csv("games.csv")
    players_df.to_csv("players.csv")
    agent_df.to_csv("agents.csv")
    player_games_df.to_csv("player_games.csv")
    player_cards.to_csv("player_cards.csv")
    player_goals.to_csv("player_goals.csv")
    player_assists.to_csv("player_assists.csv")
    player_ownGoals.to_csv("player_ownGoals.csv")
    failed_links.to_csv("failed_links.csv")
    time.sleep(random.randint(2, 10))
