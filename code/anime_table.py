import mysql.connector
import requests
import json
# database information in config.py
import config
from bs4 import BeautifulSoup
import pandas as pd
from text_process import text_process
import re
import html
from nltk.sentiment.vader import SentimentIntensityAnalyzer

with open('token.json', 'r') as f:
    auth_data = json.load(open('token.json', 'r'))

headers = {
    'Authorization' : 'Bearer ' + auth_data['access_token']
}

# Connect to the database -> the information is on the config.py file
cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.database)
cursor = cnx.cursor()

# asks for user input, an anime they want to search
anime_name = input("Enter an anime name \n")
anime_response = requests.get(f"https://api.myanimelist.net/v2/anime?q={anime_name}&limit=10", headers=headers)
anime_data = anime_response.json()

anime_names = [anime_data['data'][anime]['node']['title'] for anime in range(len(anime_data['data']))]
for i, anime_name in enumerate(anime_names):   
    print(f"{i+1}. {anime_name}")

# asking user input to type an anime and selecting the anime they specify (shows 10 results)
get_id = int(input("Please select specific Anime by it's number on the left: "))

if get_id in range(1, 11):
    selected_anime = anime_names[get_id - 1]
    print(f"Selected {selected_anime}")
else:
    print("Enter a number.")

# getting anime_id and get information using api call
def get_anime_id():    
    #using json beautifier to get the data from the response 
    anime_id = anime_data['data'][get_id - 1]['node']['id'] 

    if 'data' not in anime_data or len(anime_data['data']) == 0:
        print("Error: No anime found. ")

    response = requests.get(f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,start_date,genres,mean", headers=headers)
    anime = response.json()

    #getting data using the json data (tags)
    title = anime['title']
    anime_id = anime['id']
    airing_date = anime['start_date']
    genres = ', '.join([genre['name'] for genre in anime['genres']])
    score = anime['mean']

    #make a query to using sql commands
    query = "INSERT INTO anime (anime_id, name, year_of_release, genre, score) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE score=VALUES(score)"
    values = (anime_id, title, airing_date, genres, score)
    cursor.execute(query, values)
    cnx.commit()

    # Fetch and print the results
    for result in cursor:
        print(result)
        
    return anime_id 

#function to get the forum_ids from the data we got from get_anime_id
def get_forum_ids_scraper(anime_id):
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
        # because it shows 50 forum topics per page 
        shows += 50
        page_num += 1
        
    return all_t_id


#function to get data for forum_ids table 
def get_forum_id():
    anime_id = get_anime_id()
    forum_ids = get_forum_ids_scraper(anime_id)
    for ids in forum_ids: 
        url = f"https://api.myanimelist.net/v2/forum/topic/{ids}"
        response = requests.get(url, headers=headers)
        forum_titles = response.json()
        forum_title = forum_titles['data']['title']
        
        query = "INSERT INTO forum_ids (forum_id, anime_id, forum_title) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE forum_title=VALUES(forum_title)"
        values = (ids, anime_id, forum_title)
        cursor.execute(query, values)
        cnx.commit()

def get_comments():
    limit = 100
    forum_ids = get_forum_ids_scraper(get_anime_id())
    comments = {'forum_id': [], 'comment_id': [], 'message': [], 'cleaned_message': [], 'sentiment_score': []}

    for forum_id in forum_ids:
        offset = 0
        while True:
            response = requests.get(f"https://api.myanimelist.net/v2/forum/topic/{forum_id}?limit={limit}&offset={offset}", headers=headers)
            forum_data = response.json()
            posts = forum_data['data']['posts']
            if not posts:
                break
            comment_ids = [post['id'] for post in posts]
            bodies = [html.unescape(re.sub(r'\[yt\].*?\[/yt\]|\[img\].*?\[/img\]|\[.*?\]|\t|\n|\r|\xa0|<[^<]+?>', '', post['body'])) for post in posts]
            cleaned_messages = [text_process(body) for body in bodies]
            # Calculate sentiment score for each comment
            sentiment_scores = [get_sentiment_score(text) for text in cleaned_messages]
            comments['forum_id'].extend([forum_id] * len(posts))
            comments['comment_id'].extend(comment_ids)
            comments['message'].extend(bodies)
            comments['cleaned_message'].extend(cleaned_messages)            
            comments['sentiment_score'].extend(sentiment_scores)
            if len(posts) < limit:
                break
            offset += limit

    df = pd.DataFrame(comments)
    print(df.head())
    df.to_csv('cleaned_forum_data.csv', index=False)
    for index, row, in df.iterrows():
        original_text = row['message'].replace("'", "''")
        cleaned_text = row['cleaned_message'].replace("'", "''")
        insert_query = f"""
        INSERT INTO comments (comment_id, forum_id, original_text, cleaned_text, sentiment_score)
         VALUES ({row['comment_id']}, {row['forum_id']}, '{original_text}', '{cleaned_text}', {row['sentiment_score']}) ON DUPLICATE KEY UPDATE sentiment_score=VALUES(sentiment_score)
        """
        cursor.execute(insert_query)

    # make query to select from comments and do analysis 
    query = """SELECT cleaned_text, sentiment_score FROM comments"""
    cnx.commit()

# Retrieve the data from the clean_message column in the comments table

def get_sentiment_score(text):
    query = """SELECT cleaned_text FROM comments"""
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the results to a Pandas DataFrame
    df = pd.DataFrame(results, columns=['cleaned_message'])

    # Define the get_sentiment_score function
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(str(text))['compound']


def main():
    get_comments()
    # any other functions to execute

if __name__ == '__main__':
    main()
    
# Close the cursor and connection
cursor.close()
cnx.close()
