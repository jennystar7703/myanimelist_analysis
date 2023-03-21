#function to get data for forum_ids table 
def get_forum_id():
    anime_id = get_anime_id()
    forum_ids = get_forum_ids_scraper(anime_id)
    for ids in forum_ids: 
        url = f"https://api.myanimelist.net/v2/forum/topic/{ids}"
        response = requests.get(url, headers=headers)
        forum_titles = response.json()
        forum_title = forum_titles['data']['title']
        
        query = "INSERT IGNORE INTO forum_ids (forum_id, anime_id, forum_title) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE forum_title=VALUES(forum_title)"
        values = (ids, anime_id, forum_title)
        cursor.execute(query, values)
        cnx.commit()