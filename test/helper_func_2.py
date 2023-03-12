import requests
import json

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization': 'Bearer ' + auth_data['access_token']
}

def get_anime_data(name):
    response = requests.get(f"https://api.myanimelist.net/v2/anime?q={name}&limit=10", headers=headers)
    data = response.json()
    if 'data' not in data or len(data['data']) == 0:
        return None
    return data

def select_anime():
    data = None
    while not data:
        name = input("Enter an anime name: ")
        data = get_anime_data(name)
        if not data:
            print("Error: No anime found. ")
    anime_names = [anime['node']['title'] for anime in data['data']]
    for i, anime_name in enumerate(anime_names):
        print(f"{i+1}. {anime_name}")
    while True:
        try:
            get_id = int(input("Please select specific Anime by it's number on the left: "))
            if 1 <= get_id <= len(anime_names):
                selected_anime = anime_names[get_id - 1]
                anime_id = data['data'][get_id - 1]['node']['id']
                return selected_anime, anime_id
        except ValueError:
            pass
        print("Invalid selection. Please enter a number.")

def build_forum_url(anime_id):
    return f"https://myanimelist.net/forum/?animeid={anime_id}&topic=episode"

def main():
    selected_anime, anime_id = select_anime()
    forum_url = build_forum_url(anime_id)
    print(f"Selected {selected_anime}")
    print(f"Forum URL: {forum_url}")

if __name__ == '__main__':
    main()
