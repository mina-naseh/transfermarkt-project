import requests
from bs4 import BeautifulSoup
import pandas as pd

leagues_names = ['premier-league', 'laliga', 'bundesliga', 'serie-a', 'ligue-1']
countries = ['GB1', 'ES1', 'L1', 'IT1', 'FR1']
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

def convert_value(value_str):
    value_str = value_str.strip('€').strip()
    # print(value_str)

    multiplier = 1
    if value_str.endswith('bn'):
        multiplier = 1000000000
        value_str = value_str[:-2]
    elif value_str.endswith('m'):
        multiplier = 1000000
        value_str = value_str[:-1]

    value = float(value_str) * multiplier

    return int(round(value))

headers = {'User-Agent': 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

club_name = []
club_link = []
club_id = []
league = []
season = []
club_age = []
club_tmv = []

for league_name, country in zip(leagues_names, countries):
    for year in years:

        url = f'https://www.transfermarkt.com/{league_name}/startseite/wettbewerb/{country}/plus/?saison_id={year}'
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find("table", {"class": "items"})

        rows = table.find_all("tr")

        for row in rows:
            link = row.find("a", href=True)

            if row.find_all("a", {"title": True}):

                header = soup.find('header', {'class': 'data-header'})
                div = header.find('div', {'class': 'data-header__headline-container'})
                h1 = div.find('h1', {'class': 'data-header__headline-wrapper data-header__headline-wrapper--oswald'})
                league.append(h1.text.strip())

                club_id.append(link["href"].split("/")[4])
                club_age.append(row.find_all("td")[3].text.strip())
                club_tmv.append(convert_value(row.find_all("td")[6].text.strip()))
                club_name.append(row.find_all("a", {"title": True})[0]["title"])
                club_link.append('https://www.transfermarkt.com' + link["href"])
                season.append(year)

dict = {'club_name': club_name, 'club_link': club_link, 'club_id': club_id,
        'league': league, 'season': season, 'club_age': club_age, 'club_tmv': club_tmv} 

df = pd.DataFrame(dict)

df.to_csv('df.csv')