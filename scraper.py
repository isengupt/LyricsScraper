
import pandas as pd
import numpy as np
import re
from datetime import datetime
import json
import nltk


from sklearn.feature_extraction.text import CountVectorizer


from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import unicodedata

nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from langdetect import detect





def first_process(text):
    
    # lowercase
    text=text.lower()
    
    #remove tags
  
    text=re.sub("","",text)
     
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    return text

def pre_process(text):

    text = text.lower()
    text = text.replace("\n",".")
    #text = re.sub("&lt;/?*?&gt;", " &lt:&gt; ", text)
    #text = re.sub("(\\d|\\W)+"," ",text)

    return text
corpus = []

#### get different keywords by date window maybe 5 to 10 days

data = []

with open("long_data.ndjson", 'r') as infile:

    data = [json.loads(line) for line in infile]

print(len(data))

#print(data['songs'])
for song in data:
    #print(song['date'])
    #sprint(song['lyrics'])
 
    song['lyrics'] = pre_process(song['lyrics'])
    song['lyrics'] = first_process(song['lyrics'])
    if (len(song['lyrics'].strip()) == 0):
        data.remove(song)
        continue
    if (len(song['date']) != 10):
        print(len(song['date']))
    

print(len(data))


         

   

      

       
    #if (song['date']):
        
        #print(song['date'])
        #song['date'] = datetime.strptime(song['date'], "%Y-%m-%d")
    #else:
     #   data['songs'].remove(song)

#for song in data['songs']: 
#    if (song['lyrics']):
#        song['lyrics'] = pre_process(song['lyrics'])



sortedArray = sorted(
   data,
key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=True
)

song_file = {
    "songs": sortedArray
}


with open('long.json', 'w') as f:  
  json.dump(song_file, f)



#print(len(sortedArray))





