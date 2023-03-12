import mysql.connector
import requests
import json
import config
import anime_table


with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

# Connect to the database
cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.database)
cursor = cnx.cursor()

anime_id = get_forum_id()