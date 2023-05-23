import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

required_leagues = ['2022 World Cup', 'UEFA Champions League', 'Premier League',
                    'World Cup 2018', 'Bundesliga', 'LaLiga', 'Serie A', 'Ligue 1']

player_info = pd.DataFrame(columns=['player_name', 'player_id',
                           'team_name', 'league', 'birthdate', 'height', 'main_position', 'national_team', 'agent'])

player_game_info = pd.DataFrame(
    columns=['player_id', 'league_name', 'matchday', 'date', 'home_team', 'away_team', 'result', 'position', 'goals', 'assists', 'own_goals', 'yellow_cards', 'second_yellow_cards', 'red_cards', 'substitution_on', 'substitution_off', 'minutes_played', 'bench', 'injury', 'not_squad'])
failed_links = pd.DataFrame(columns=['url'])


def extract_player_details(url, year, player_name, player_id):
    global player_info
    global player_game_info
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
        none = [None] * 4
        height, main_position, national_team, agent = none
        li_tags = soup.find(
            'div', class_="data-header__info-box").find_all('li')
        for a in range(len(li_tags)):
            info_type = li_tags[a]
            if "Position" in info_type.text.strip():
                main_position = info_type.find('span').text.strip()
            elif "Height" in info_type.text.strip():
                height = info_type.find('span').text.strip().replace(
                    "m", "").replace(",", "")
            elif "international" in info_type.text.strip():
                national_team = info_type.find('span').text.strip()
            elif "Agent" in info_type.text.strip():
                agent = info_type.find('span').text.strip()
            try:
                team_info = soup.find(
                    'div', class_="data-header__box--big").find('div', class_="data-header__club-info")
                team_name = team_info.find(
                    'span', class_="data-header__club").text.strip()
                team_league = team_info.find(
                    'span', class_="data-header__league").text.strip()
            except:
                team_name = None
                team_league = None

            box = soup.find_all('div', class_="box")
        for i in range(len(box)):
            league_div = box[i].find('div', class_="table-header")
            if league_div is None:
                continue
            league_name = league_div.find('a').text.strip()
            if league_name is None:
                continue
            if league_name in required_leagues:
                table = league_div.parent.find('tbody').find_all('tr')
                for t in range(len(table)):
                    td = table[t].find_all('td')
                    if len(td) > 4:
                        matchday = td[0].text.strip()
                        date = td[1].text
                        home_team = td[3].find('a')['title']
                        away_team = td[5].find('a')['title']
                        result = td[6].find('a').text
                        none = [None] * 13
                        position, goals, assists, own_goals, yellow_cards, second_yellow_cards, red_cards, substitution_on, substitution_off, minutes_played, bench, injury, not_squad = none
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
                            minutes_played = None if td[16].text == "" else td[16].text.replace(
                                "'", "")
                        else:
                            status = td[7].text
                            if "bench" in status:
                                bench = td[7].text
                            elif status == "Not in squad":
                                not_squad = td[7].text
                            else:
                                injury = td[7].text

                    player_game_info = player_game_info._append({
                        'player_id': player_id,
                        'league_name': league_name,
                        'matchday': matchday,
                        'date': date,
                        'home_team': home_team,
                        'away_team': away_team,
                        'result': result,
                        'position': position,
                        'goals': goals,
                        'assists': assists,
                        'own_goals': own_goals,
                        'yellow_cards': yellow_cards,
                        'second_yellow_cards': second_yellow_cards,
                        'red_cards': red_cards,
                        'substitution_on': substitution_on,
                        'substitution_off': substitution_off,
                        'minutes_played': minutes_played,
                        'bench': bench,
                        'injury': injury,
                        'not_squad': not_squad
                    }, ignore_index=True)
        player_info = player_info._append({
            'player_name': player_name,
            'player_id': player_id,
            'team_name': team_name,
            'league': team_league,
            'birthdate': birthdate,
            'height': height,
            'main_position': main_position,
            'national_team': national_team,
            'agent': agent,
            'year': year
        }, ignore_index=True)
    except Exception as e:
        print(f"Error occurred for {url}: {e}")
        failed_links = failed_links._append({
            'url': url,
        }, ignore_index=True)


player_df = pd.read_json("players_club_history.json")


for i in range(len(player_df)):
    name = player_df['player_name'][i]
    id = player_df['player_id'][i]
    year = player_df['year'][i]
    url = f"https://www.transfermarkt.com/{name}/leistungsdatendetails/spieler/{id}/plus/1?saison={year}&verein=&liga=&wettbewerb=&pos=&trainer_id="
    print(i, name, year, player_df['team_id'][i], url)
    extract_player_details(url, year, name, id)
    player_info.to_csv("players_info.csv")
    player_game_info.to_csv("player_game_info.csv")
    failed_links.to_csv("failed_links.csv")
