import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import pandas as pd
from threading import Thread
import json
import numpy as np
import bs4
from langdetect import detect
import urllib
import re
import os



from bs4 import BeautifulSoup
from urllib.request import urlretrieve 
from urllib.request import urlopen, Request

######################################################################
########### File containing all functions to do with search #########
#####################################################################

base = "https://api.genius.com"
client_access_token = "h-R8aiVgb9lEoIr9ICqLrjBNbdt_RBCaBQ8dUN8aJTN2QaKBxdoXtcMqlJj4y_-j"

all_songs_data = []

def scrape_song(url_path):

    html = urlopen(url_path)

    soup = BeautifulSoup(html, 'lxml')

    links = soup.find("a")

  

def get_json(path, params=None, headers=None):
    '''Send request and get response in json format.'''

    # Generate request URL
    requrl = '/'.join([base, path])
    token = "Bearer {}".format(client_access_token)
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    # Get response object from querying genius api
    response = requests.get(url=requrl, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def search(artist_name):
    '''Search Genius API via artist name.'''
    search = "search?q="
    query = base + search + urllib.parse.quote(artist_name)
    request = urllib.request.Request(query)

    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")

    response = urllib.request.urlopen(request, timeout=3)
    raw = response.read()
    data = json.loads(raw)['response']['hits']

    for item in data:
        # Print the artist and title of each result
        print(item['result']['primary_artist']['name']
              + ': ' + item['result']['title'])


def search_artist(artist_id):
    '''Search meta data about artist Genius API via Artist ID.'''
    search = "artists/"
    path = search + str(artist_id)
    request = get_json(path)
    data = request['response']['artist']

    print(data["followers_count"])
    # Lots of information we can scrape regarding the artist, check keys
    return data["followers_count"] # number of followers

def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
       
    return lyrics

def search_songs(id):

    '''Search meta data about artist Genius API via Artist ID.'''
    search = "songs/"
    path = search + str(id)
    try:
        request = get_json(path)
        release_date = request['response']['song']['release_date']
        url_path = request['response']['song']['url']
        image_url = request['response']['song']['song_art_image_url']
        title = request['response']['song']['title']
        full_title = request['response']['song']['full_title']
        record_loc = request['response']['song']['recording_location']
        #print(url_path)
        if (release_date):
            song_data = {
            "title": title,
            "date": release_date,
            "image": image_url,
            "path": url_path,
            "record_loc": record_loc,
            "lyrics": scrape_song_lyrics(url_path) 

            }
            #print(song_data)
          
            all_songs_data.append(song_data)
            print(len(all_songs_data))
            info_file.write(json.dumps(song_data) + "\n")
            return song_data
        

    except requests.exceptions.RequestException as e: 
        #print("Not found")
        return {}
      
    
    #data = request['response']['song']['release_date']

    #print(data)5909351
#for i in range(0, 10, 1):
#   search_songs(i) 

num_list = list(range(5909351, 5909351 - 50000, -1))
#print(num_list)
threadpool = ThreadPool(processes=8)
info_file =  open('lona.ndjson', 'w') 
results = threadpool.map(search_songs, num_list)


song_file = {
    "songs": all_songs_data
}








# DEMO
#print(scrape_song_lyrics('https://genius.com/Lana-del-rey-young-and-beautiful-lyrics'))