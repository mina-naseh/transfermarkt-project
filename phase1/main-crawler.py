import requests
from bs4 import BeautifulSoup

from crawlers.player_crawler import crawl_player_detail_page



base_url = 'https://www.transfermarkt.com'
club_url = f'{base_url}/burnley-fc/kader/verein/1132/plus/1/galerie/0?saison_id=2021'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }


#### CLUB(PLAYERS LIST) PAGE
response = requests.get(club_url, headers=headers)
content = BeautifulSoup(response.text, 'html.parser')
players_selectors = content.select('table.items > tbody > tr')


for player in players_selectors:
    compact_player_href = player.select_one('td.posrela td.hauptlink a').get("href")
    detailed_player_href = f"{base_url}{compact_player_href.replace('profil', 'leistungsdatendetails')}/plus/1?saison=&verein=&liga=&wettbewerb=&pos=&trainer_id="
    crawl_player_detail_page(detailed_player_href)
