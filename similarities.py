
import pandas as pd
import numpy as np
import re
from datetime import datetime
import json
import nltk

from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

def get_stop_words(stop_file_path):

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


stopwords = get_stop_words('resources/stopwords.txt')
data = []
date_dict ={}
with open('long_clean.json') as f:
  data = json.load(f)

print(len(data['songs']))
#print(data['songs']) datetime.strptime(song['date'], "%Y-%m-%d")
for song in data['songs']:

    #for dt in date_dict.keys():
    addingDate = datetime.strptime(song['date'], "%Y-%m-%d")

    found = False
    for dt in date_dict.keys():
        currDate = datetime.strptime(dt, "%Y-%m-%d")
        if (abs((addingDate - currDate).days) < 21):

            date_dict[dt].append(song)
            found = True
            continue
    if (found == False):
        #print(song['date'])
        date_dict[song['date']] = []
        date_dict[song['date']].append(song)  
    

#print(date_dict)
for date in date_dict.keys():
    print("Check date: ", date)
    for song in date_dict[date]:
        print(song['date'])
    




with open('dates_dict.json', 'w') as f:  
   json.dump(date_dict, f)
   
    #if (song['date'] in date_dict):
    #    date_dict[song['date']].append(song)
    
    #else:
    #  date_dict[song['date']] = []
    #  date_dict[song['date']].append(song)  
    
   
#print(date_dict)

date1 = datetime.strptime("2014-03-02", "%Y-%m-%d")
date2 = datetime.strptime("2013-08-01", "%Y-%m-%d")
difference = date2 - date1
seconds_in_day = 24 * 60 * 60
print(difference.days)
