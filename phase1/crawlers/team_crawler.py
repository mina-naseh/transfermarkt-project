import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
base_url = 'https://www.transfermarkt.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

teams_df = pd.DataFrame(columns=[
                        "id", "name", "age", "tmv", "year", "league_name"])
leagues_df = pd.DataFrame({'name': ['premier-league', 'primera-division', 'bundesliga',
                                    'serie-a', 'ligue-1'], 'id': ['GB1', 'ES1', 'L1', 'IT1', 'FR1']})
years = [2017, 2018, 2019, 2020, 2021]


def extract_teams(url, year, league_name):
    global teams_df
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tr = soup.find(
        'div', class_="responsive-table").find('tbody').find_all('tr')
    for i in range(len(tr)):
        td = tr[i].find_all('td')
        href = td[1].find('a')['href']
        name = extract_name(href)
        id = extract_id(href)
        age = td[3].text
        tmv = td[6].text.replace("€", "")
        teams_df = teams_df.append({
            "id": id,
            "name": name,
            "age": age,
            "tmv": tmv,
            "year": year,
            "league_name": league_name
        }, ignore_index=True)
    return "OK"


def extract_id(a_tag):
    sp = a_tag.split('/')[4]
    numbers = re.findall('\d+', sp)
    result = ''.join(numbers)
    return result


def extract_name(a_tag):
    sp = a_tag.split('/')[1]
    result = ''.join(sp)
    return result


for i in range(len(leagues_df)):
    name = leagues_df['name'][i]
    id = leagues_df['id'][i]
    for y in range(len(years)):
        year = years[y]
        url = f"https://www.transfermarkt.com/{name}/startseite/wettbewerb/{id}/plus/?saison_id={year}"
        extract_teams(url, years[y], leagues_df['name'][i])
        print(leagues_df['name'][i], years[y])
teams_df.to_json("teams_data")
