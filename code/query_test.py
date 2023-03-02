import sqlite3
import requests 
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}


def get_forum_id(anime_name):
    anime_name = input("enter an anime name \n")
    anime_response = requests.get(f"https://api.myanimelist.net/v2/anime?q={anime_name}&limit=10", headers=headers)
    anime_data = anime_response.json()
    for anime in anime_data:
        select_anime = input(f"{anime} + {anime_data} Please Specify which one: Num")

    if 'data' not in anime_data or len(anime_data['data']) == 0:
        print("Error: No anime found. ")

    
    anime_id = anime_data['data'][0]['node']['id']
    response = requests.get(f"https://api.myanimelist.net/v2/forum/topics?q={anime_id}&limit=10", headers=headers)

    forum_data = response.json()
    print(forum_data)


get_forum_id("bleach")
def database():
    conn = sqlite3.connect('forum_posts.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS topic_info (
            forum_id INTEGER PRIMARY KEY AUTOINCREMENT,
            forum_title TEXT,
            date TEXT,
            FOREIGN KEY (forum_id) REFERENCES forum_comments(forum_id)
        )
        ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS forum_comments (
            forum_id INTEGER,
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_text TEXT,
            FOREIGN KEY (forum_id) REFERENCES topic_info(forum_id)       
        )
        ''')

    for texts in forum_data['data']:
        c.execute("""
            INSERT OR IGNORE INTO topic_info (forum_id, forum_title, date)
            VALUES (?, ?, ?)
        """, (texts['id'], texts['title'], texts['created_at']))

    conn.commit()
    conn.close()