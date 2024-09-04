import requests
import json
import re
from bs4 import BeautifulSoup
from rich.console import Console
console = Console()

base_url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&kontinent_id=0&galerie=1&page="
URLS = [base_url + str(page) for page in range(1, 501)]

# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def extract_money(text):
    # Extract the number and the multiplier (m for million, b for billion, etc.)
    match = re.match(r"[€$£]?([\d,.]+)([mbk]?)", text.strip(), re.IGNORECASE)
    if not match:
        return None

    # Get the numeric value and multiplier
    number_str, multiplier = match.groups()

    # Remove any commas
    number_str = number_str.replace(",", "")

    # Convert the number to a float
    number = float(number_str)

    # Apply the multiplier
    if multiplier.lower() == 'm':
        number *= 1_000_000
    elif multiplier.lower() == 'b':
        number *= 1_000_000_000
    elif multiplier.lower() == 'k':
        number *= 1_000

    # Convert to an integer
    return int(number)


def crawl(url) -> dict:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    selector = '#yw1 > table > tbody > tr'
    player_roi = soup.select(f'{selector} > td:nth-child(1) > table > tr')
    gallery_url = soup.select_one('#wertvollstespieler > div > div > div.responsive-table > div.galerie-box > div > img').get('src')
    player_url = player_roi[0].select_one('td:nth-child(1) > a > img').get('src')
    player = player_roi[0].select_one('td:nth-child(1) > a > img').get('title')
    position = player_roi[1].select_one('td').get_text()
    age = soup.select_one(f'{selector} > td:nth-child(2)').get_text()
    nationalities = []
    for element in soup.select_one(f'{selector} > td:nth-child(3)').select('img'):
        nationality_url = element.get('src')
        nationality = element.get('title')
        nationalities.append({'nationality_url': nationality_url, 'nationalty': nationality})
    club_image_url = soup.select_one(f'{selector} > td:nth-child(4) > a > img').get('src')
    club = soup.select_one(f'{selector} > td:nth-child(4) > a > img').get('title')
    market_value = soup.select_one(f'{selector} > td.rechts.hauptlink').get_text()
    matches = soup.select_one(f'{selector} > td:nth-child(6)').get_text()
    goals = soup.select_one(f'{selector} > td:nth-child(7)').get_text()
    own_goals = soup.select_one(f'{selector} > td:nth-child(8)').get_text()
    assists = soup.select_one(f'{selector} > td:nth-child(9)').get_text()
    yellow_cards = soup.select_one(f'{selector} > td:nth-child(10)').get_text()
    second_yellow_cards = soup.select_one(f'{selector} > td:nth-child(11)').get_text()
    red_cards = soup.select_one(f'{selector} > td:nth-child(12)').get_text()
    substitution_on = soup.select_one(f'{selector} > td:nth-child(13)').get_text()
    substitution_off = soup.select_one(f'{selector} > td:nth-child(14)').get_text()

    return dict(
        gallery_url=gallery_url,
        player_url=player_url,
        player=player,
        position=position,
        age=int(age),
        nationalities=nationalities,
        club_image_url=club_image_url,
        club=club,
        market_value=extract_money(market_value),
        matches=int(matches),
        goals=int(goals),
        own_goals=int(own_goals),
        assists=int(assists),
        yellow_cards=int(yellow_cards),
        second_yellow_cards=int(second_yellow_cards),
        red_cards=int(red_cards),
        substitution_on=int(substitution_on),
        substitution_off=int(substitution_off),
    )


if __name__ == '__main__':
    data = []
    for ix, url in enumerate(URLS, 1):
        console.print(f'Crawling page -> {ix}/{len(URLS)}')
        try:
            data.append(crawl(url=url))
        except Exception as e:
            console.print(f'An exception occurred while crawling page ->{ix}/{len(URLS)}\n\nException:{e}')

    console.print('Writing data to file...')
    with open('player_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    console.print('All process is done!')
