import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import re

drama_info = defaultdict(list)
url_base = "https://mydramalist.com/shows/top_korean_dramas?page="

def get_drama_list(url):
    # Load the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get list of all the dramas in the page
    mainbody = soup.find('div', class_="col-lg-8 col-md-8")
    dramas = mainbody.find_all('div', class_='box-body')
    return dramas

def extract_info(drama):
    rank = drama.find('div', class_='ranking pull-right').text

    # Extract Title: there is newline at the end so .strip()
    title = drama.find('h6', class_='text-primary title').text.strip()

    # Image url given by https://i.mydramalist.com
    img = drama.find('img')['data-src']

    # Both year and ep given in the form of "Korean Drama - {year}, {ep} episodes"
    year_and_ep = drama.find('span', class_='text-muted').text

    # Therefore, find all int and assign to year and ep
    year, ep = [int(s) for s in re.findall(r'\d+', year_and_ep)]

    rating = drama.find('span', class_='p-l-xs score').text

    # # Return the list of info
    # return [rank, title, img, year, ep, rating]

    drama_info['rank'].append(rank)
    drama_info['title'].append(title)
    drama_info['img'].append(img)
    drama_info['year'].append(year)
    drama_info['ep'].append(ep)
    drama_info['rating'].append(rating)

for n in range(1, 6):
    url = url_base + f'{n}'
    dramas = get_drama_list(url)
    for drama in dramas:
        extract_info(drama)

drama_info = pd.DataFrame.from_dict(drama_info)
drama_info.to_csv('drama_db.csv', index=False)