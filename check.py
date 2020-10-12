import json
import requests


songs_dict = {}
per_songs = []
with open('raked_dict_upsdated.json') as f:
  songs_dict = json.load(f)



for dt in songs_dict.keys():
    

    for song in songs_dict[dt]['songs']:
        song_entry = {}
        song_entry['root_date'] = dt
        song_entry['information'] = song
        song_entry['raked_words'] = songs_dict[dt]['key_words']
    

        if(song['record_loc']):
            response = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + song['record_loc'] +"&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyCY3b8hR2rD5K3WkmhN4NthRo3XId9bclk")
            if (response.json()['status'] == "OK"):
                
                print(response.json())
                lat = response.json()['candidates'][0]['geometry']['location']['lat']
                lng  = response.json()['candidates'][0]['geometry']['location']['lng']
                song_entry['location'] = { 'lat': lat, 'lng': lng }
                per_songs.append(song_entry)


print(per_songs[0])

new_dict = {
    'songs': per_songs
}

with open('per_song.json', 'w') as f:  
   json.dump(new_dict, f)

        #print(song)
        #if (song['record_loc']):
            #print(song['record_loc']) 

            #response = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + song['record_loc'] +"&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyCY3b8hR2rD5K3WkmhN4NthRo3XId9bclk")

            #print(response.json())
            #try:
    #    for ds in songs_dict[dt]['key_words'].keys():
    #        print(dt)
    #        print(songs_dict[dt]['key_words'][ds])

    #except: 
    #    print("No key words found")
#AIzaSyCY3b8hR2rD5K3WkmhN4NthRo3XId9bclk

#response = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyCY3b8hR2rD5K3WkmhN4NthRo3XId9bclk")

#print(response.json())