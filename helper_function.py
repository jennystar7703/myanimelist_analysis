import sqlite3
import requests 
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

def get_anime_data(input_name):
    anime_response = requests.get(f"https://api.myanimelist.net/v2/anime?q={input_name}&limit=10", headers=headers)
    anime_data = anime_response.json()

    if 'data' not in anime_data or len(anime_data['data']) == 0:
        print("Error: No anime found. ")
        return None

    return anime_data

def print_anime_list(anime_data):
    anime_names = [anime_data['data'][anime]['node']['title'] for anime in range(1,10)]
    for i, anime_name in enumerate(anime_names):   
        print(f"{i+1}. {anime_name}")

def get_forum_id():
    #get user input of anime and use API call to show top 10 results
    input_name = input("Enter an anime name: ")
    anime_data = get_anime_data(input_name)

    if anime_data is None:
        return

    # print out results
    print_anime_list(anime_data)

    get_id = int(input("Please select specific Anime by it's number on the left: "))
    if get_id in range(1, 11):
        selected_anime = anime_data['data'][get_id]['node']['title']
        print(f"Selected {selected_anime}")
    else:
        print("Enter a number.")
        return

    anime_id = anime_data['data'][get_id]['node']['id'] 
    print(f"https://myanimelist.net/forum/?animeid={anime_id}&topic=episode")

get_forum_id()