import requests
from bs4 import BeautifulSoup



base_url = 'https://www.transfermarkt.com'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }
seasons = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
countries = [    
    {"name":"Germany", "id":40},
    {"name":"France", "id":50},
    {"name":"Italy", "id":75},
    {"name":"Spain", "id":157},
    {"name":"England", "id":189},
]
