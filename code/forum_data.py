import requests 
import json 
import pandas as pd 

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

t_id = ['2066087', '2066086', '2064811', '2063298', '2061761', '2060259', '2058951', '2057673', '2056377', '2055115', '2053673', '2052248', '2050403']

bodies = []
for ids in t_id:
    response = requests.get(f"https://api.myanimelist.net/v2/forum/topic/{ids}?limit=100", headers=headers)
    forum_data = response.json()
    bodies += [item['body'] for item in forum_data['data']['posts']]

df = pd.DataFrame(bodies)
df.to_csv('forum_data.csv', index=False, header=False, mode='a')

# 2023/02/19