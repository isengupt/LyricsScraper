import json
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from gensim.summarization import keywords

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import unicodedata
import RAKE
from multi_rake import Rake

import operator
rake = Rake()
def replace_ptbr_char_by_word(word):
 
    word = str(word)
    word = unicodedata.normalize('NFKD', word).encode('ASCII','ignore').decode('ASCII')
    return word

def remove_pt_br_char_by_text(text):
  
    text = str(text)
    text = ''.join(x for x in text if x.isprintable())


    #text = " ".join(replace_ptbr_char_by_word(word) for word in text.split() if word not in stopwords)
    return text

def pre_process(text):
    
    # lowercase
    text=text.lower()
    
    #remove tags
    text=re.sub("","",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    return text

def get_stop_words(stop_file_path):

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


stopwords = get_stop_words('resources/stopwords.txt')



songs_dict = {}

stop_dir = "./resources/SmartStoplist.txt"
rake_object = RAKE.Rake(stop_dir)



new_dict = {}


with open('dates_dict.json') as f:
  songs_dict = json.load(f)

#print(songs_dict)

for dt in songs_dict.keys():


    new_dict[dt] = {}
    wordsData = ""
    new_dict[dt]['songs'] = songs_dict[dt] 
    for song in songs_dict[dt]:
        #print(song['lyrics'])
        song['lyrics'] = remove_pt_br_char_by_text(song['lyrics'])
        #song['lyrics'] = pre_process(song['lyrics'])
        wordsData = wordsData + "." + song['lyrics']

    print(len(wordsData))
    new_dict[dt]['words'] = wordsData
    important_words = {}
    if (len(wordsData) < 5000000):


            keyw = rake_object.run(wordsData)
            important_words['rake1'] = keyw[:10]

            print(dt)
            print ("Normal Rake: ", keyw[:10])

            gen1 = keywords(wordsData,words = 10,scores = True, lemmatize = True)
            important_words['gen1'] = gen1
            print ("Gen: ", gen1)

            rake_keys = rake.apply(wordsData)
            important_words['rake2'] = rake_keys[:10]

            print("Second Rake:", rake_keys[:10])
    
    new_dict[dt]['key_words'] = important_words
    
    
  



with open('raked_dict_upssdated.json', 'w') as f:  
   json.dump(new_dict, f)
       # print(dt)
       # print(wordsData)
#        try
#        cv=CountVectorizer(max_df=0.85,stop_words=stopwords,max_features=10000)
 #       dt_mat = cv.fit_transform(wordsData)
        #print(list(cv.vocabulary_.keys())[:10])




#print(len(songs_dict.keys()))