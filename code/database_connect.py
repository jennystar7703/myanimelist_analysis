import mysql.connector
import requests
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

host = 'localhost'
database = 'myanimelist'
user = 'jenny'
password = '1234'

# Connect to the database
cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = cnx.cursor()

def get_forum_id():
    anime_name = input("enter an anime name \n")
    anime_response = requests.get(f"https://api.myanimelist.net/v2/anime?q={anime_name}&limit=10", headers=headers)
    anime_data = anime_response.json()

    anime_names = [anime_data['data'][anime]['node']['title'] for anime in range(1,10)]
    for i, anime_name in enumerate(anime_names):   
        print(f"{i+1}. {anime_name}")
    
    get_id = int(input("Please select specific Anime by it's number on the left: "))
    if get_id in range(1, 11):
        selected_anime = anime_names[get_id - 1]
        print(f"Selected {selected_anime}")
    else:
        print("Enter a number.")
    
    anime_id = anime_data['data'][get_id]['node']['id'] 

    if 'data' not in anime_data or len(anime_data['data']) == 0:
        print("Error: No anime found. ")

    
    anime_id = anime_data['data'][0]['node']['id']
    response = requests.get(f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,start_date,genres,mean", headers=headers)

    anime = response.json()

    title = anime['title']
    anime_id = anime['id']
    airing_date = anime['start_date']
    genres = ', '.join([genre['name'] for genre in anime['genres']])
    score = anime['mean']

    query = "INSERT INTO anime (anime_id, name, year_of_release, genre, score) VALUES (%s, %s, %s, %s, %s)"
    values = (anime_id, title, airing_date, genres, score)
    cursor.execute(query, values)
    cnx.commit()

    # Fetch and print the results
    for result in cursor:
        print(result)
        
get_forum_id()

# Close the cursor and connection
cursor.close()
cnx.close()
