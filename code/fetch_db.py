import sqlite3
import requests 
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

response = requests.get("https://api.myanimelist.net/v2/users/tt7703ok/animelist?fields=list_status&limit=10", headers=headers)
data = response.json()

conn = sqlite3.connect('anime.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS anime_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        status TEXT
    )
        ''')

print(data)
for anime in data['data']:
    c.execute("""
        INSERT OR IGNORE INTO anime_list (id, name, score, status)
        VALUES   (?, ?, ?, ?)        
    """, (anime['node']['id'], anime['node']['title'], anime['list_status']['score'], anime['list_status']['status']))


conn.commit()
conn.close()