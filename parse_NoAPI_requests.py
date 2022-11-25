import requests
from typing import Union
import pandas as pd
import networkx
import matplotlib.pyplot as plt
import vk_api
from bs4 import BeautifulSoup
from boilerpy3 import extractors
import stop_words
import pymorphy2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import word_tokenize 
from PIL import Image




def get_friend_ids(user_id, token, v):
    url = 'https://api.vk.com/method/friends.get?user_id={}&access_token={}&v={}'
    json_response = requests.get(url.format(user_id, token, v)).json()
    if json_response.get('error'):
        print(json_response.get('error'))
        return list()
    return json_response['response']['items']


def get_wall_content(ids: Union[list, tuple]) -> dict:
	block_text = ['в друзья, чтобы смотреть его записи, фотографии', 'Мы обнаружили на странице']
	wall_content = dict()

	for user_id in ids:
	    url = 'https://vk.com/id'+str(user_id)
	    extractor = extractors.KeepEverythingExtractor()
	    wall_content[user_id] = ''
	    for line in extractor.get_content_from_url(url).split('\n'):
	        if len(line.split()) >= 10 and block_text[0] not in line and block_text[1] not in line:
	            wall_content[user_id] += ' ' + line
    return wall_content

def get_status_content(ids: Union[list, tuple]) -> dict:
	status_content = dict()

	for user_id in ids:
	    url = 'https://vk.com/id'+str(user_id)
	    html = requests.get(url).content
	    html = BeautifulSoup(html, 'html.parser')
	    try:
	        status = html.find_all('div', {'class':'pp_status'})[0].get_text()
	        status_content[user_id] = status
	    except:
	        status_content[user_id] = None
    return status_content

friend_ids = get_friend_ids(my_id, token, v)
wall = get_wall_content(friend_ids)
status = get_status_content(friend_ids)


wall = pd.DataFrame.from_dict(wall, orient = 'index')
wall.columns = ['wall']
status = pd.DataFrame.from_dict(status, orient = 'index')
status.columns = ['status']

df = status.join(wall)
df.to_csv('status_wall.csv', index = True, header = True)