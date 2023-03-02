import sqlite3
import requests 
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}    

anime_name = input("enter an anime name \n")
anime_response = requests.get(f"https://api.myanimelist.net/v2/anime?q={anime_name}&limit=10", headers=headers)
anime_data = anime_response.json()
print(anime_data)