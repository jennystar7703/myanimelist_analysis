import mysql.connector
import requests
import json
import config
from bs4 import BeautifulSoup

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

# Connect to the database
cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.database)
cursor = cnx.cursor()

def get_anime_id():
    anime_name = input("Enter an anime name \n")
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

    query = "INSERT INTO anime (anime_id, name, year_of_release, genre, score) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE score=VALUES(score)"
    values = (anime_id, title, airing_date, genres, score)
    cursor.execute(query, values)
    cnx.commit()

    # Fetch and print the results
    for result in cursor:
        print(result)
        
    return anime_id 

def get_forum_ids(anime_id):
    all_t_id = []
    shows = 0
    page_num = 1
    
    while True:
        # Construct the URL for the current page number
        url = f"https://myanimelist.net/forum/?animeid={anime_id}&topic=episode&show={shows}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr', {'id': lambda x: x and x.startswith('topicRow')})
        
        if not rows:
            break
        
        t_id = [row['data-topic-id'] for row in rows]
        print(f"Forum IDs for page {page_num}: {t_id}")
        all_t_id.extend(t_id)
        shows += 50
        page_num += 1
        
    return all_t_id

anime_id = get_anime_id()

forum_ids = get_forum_ids(anime_id)
for ids in forum_ids: 
    url = f"https://api.myanimelist.net/v2/forum/topic/{ids}"
    response = requests.get(url, headers=headers)
    forum_titles = response.json()
    forum_title = forum_titles['data']['title']
    
    query = "INSERT INTO forum_ids (forum_id, anime_id, forum_title) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE forum_title=VALUES(forum_title)"
    values = (ids, anime_id, forum_title)
    cursor.execute(query, values)
    cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
