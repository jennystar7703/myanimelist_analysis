Myanimelist Info

client ID :  `7c23acc964a27003ae9e2c80e2ab4c08`

```
WyqZqjPcsOXpWst7lfzyNWSOLDjZrKiFL4aMKBOTJCRGqbkzHnAt5R_ohOrcH51-EDKGaMH27eHZfpM2UfRgcimAodtHSNDi3yndcU--KfrriV9QqRon1XCnTshrsn3K
```

**goal is to ultimately use api from myanimelist.com to get information about certain forum posts with the keywords and  do a sentimental analysis on it** 

> later idea --> do web scraping to get reviews on anime and do the analysis 

Automation process (?) --> for weekly updated anime 

#### Authentication

```bash
Authorise your application by clicking here:
https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id=7c23acc964a27003ae9e2c80e2ab4c08&code_challenge=wBGteXcwlT94xXj4OLYNWaYF4V_7pbAk87bXeQRqPiUz6c719hblSdvZSY_rfJEzBl7_8XiccMXQE4VUvk6_1WJe8A7NTrUnJbbeiBlRBpzm5-pZuWA5Mk9FTBNXHW6j

Copy-paste the Authorisation Code: def50200c85914bbd4ceb3077821a607825c797f62517a672bc1bdd5a1578daf6593f2fe7e97b8cab70a1dfc701bb7ac2a90a00a7370344288c76b4e8620e650fb0ee567ebeddf0f829f7c30ca30031874c11b2872126fd4a35c923771d6506454ba852fb90d3ef592ccb15447b2a91a54d0db5570603b7f4af1457a95ca0e31522dc2d520ef58d6342eb6919de6b04beb31293da06d6b6eb6c616b5685d8aa3c0231cd9129ffa70a0c659e6fab24c7db3b6d7ca501cf4e01a3ce6e1ab88343de6c2660416db9d36dc41c4d069ff5c4bde864ea307b0f151ef2b99b81f109354b60be1517e85191847787c4cc74e9cfc0bba4c77c1df2c120db10d3cf41e2454d8e0a7a6631d92c2f1ede7eebccb217b29d6673d7b7c1f74a4211be7457218d14d222ca420a4109b811b066e39192b4032ba655ba8060d8675b2e6e1cc7cae4022bdf890aa86cea5756dde67e76a9a2e2970e4737c644027a2156fb2181aed78eb4a008c323ce4dfd2d4440bcf63bf966aaf725b15d45d115845ef615ee84bd8b8e7193b90ffe94ccf0cf348873137e0ca8424566087d0933de6da4c463a8fd74f0b108801c05579e777948c6f70e29e0de5876c5a7384f9c6fd4bc01efe111421e23b6f7e96e129b6e83404cbd3b8ce9c7c9e5068b772bb6b553772d3481a78c57428a7895c0943a8
Token generated successfully!
Token saved in "token.json"
```

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIn0.eyJhdWQiOiI3YzIzYWNjOTY0YTI3MDAzYWU5ZTJjODBlMmFiNGMwOCIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIiwiaWF0IjoxNjc2MTA5NjA2LCJuYmYiOjE2NzYxMDk2MDYsImV4cCI6MTY3ODUyODgwNiwic3ViIjoiMjEwODE5OSIsInNjb3BlcyI6W119.fKRkj-BDika--WePFqrQ-gIlMkrWJI1dclSziZouUBWJnfldwuq7exD3c52LdVIJfUP9NzHc-oPwF3G3tBWPtLSNmaXmfxYBTcKYVCja2Y72Cj-XihhPBjiWle2cadISTnDuloZPLuHVEjwThnBL7WvjzeDApoG5Nt9NqO8we83Zztq3tfl0Wu1qG4godMCToMV3b-3D0M9v54e1tZEJT-i0WhDYRTN4UlAG-AVIcPqJLscpKGx_YR1KZX28oPZB6zVVxEbaK7TzMQ751xwKSrrUZDsKYGxu7ixOBMFMInDJ_PPPcwchDE1u76egEHBU1XfwrZErlR6LVHtK16i00A
```



1. Make a query for topics (user input)

2. go through each topic --> save the forum_id onto a database  

   ```bash
   curl 'https://api.myanimelist.net/v2/forum/topics?q=love&subboard_id=2&limit=10' \
   -H 'Authorization: Bearer YOUR_TOKEN'
   ```

3. access those forum posts via api call through 

   ```bash
   curl 'https://api.myanimelist.net/v2/forum/topic/{database_topic_id}' \
   -H 'Authorization: Bearer YOUR_TOKEN'
   ```

4. 

```bash
curl 'https://api.myanimelist.net/v2/anime/41467?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics' \
-H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIn0.eyJhdWQiOiI3YzIzYWNjOTY0YTI3MDAzYWU5ZTJjODBlMmFiNGMwOCIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIiwiaWF0IjoxNjc2MTA5NjA2LCJuYmYiOjE2NzYxMDk2MDYsImV4cCI6MTY3ODUyODgwNiwic3ViIjoiMjEwODE5OSIsInNjb3BlcyI6W119.fKRkj-BDika--WePFqrQ-gIlMkrWJI1dclSziZouUBWJnfldwuq7exD3c52LdVIJfUP9NzHc-oPwF3G3tBWPtLSNmaXmfxYBTcKYVCja2Y72Cj-XihhPBjiWle2cadISTnDuloZPLuHVEjwThnBL7WvjzeDApoG5Nt9NqO8we83Zztq3tfl0Wu1qG4godMCToMV3b-3D0M9v54e1tZEJT-i0WhDYRTN4UlAG-AVIcPqJLscpKGx_YR1KZX28oPZB6zVVxEbaK7TzMQ751xwKSrrUZDsKYGxu7ixOBMFMInDJ_PPPcwchDE1u76egEHBU1XfwrZErlR6LVHtK16i00A'
```



--> 

1. user input must get it from the GET endpoint `/anime` --> anime id 

   ```bash
   curl 'https://api.myanimelist.net/v2/anime?
   q=USER_INPUT&limit=4' \
   ```

2. search for that result in forums -->need anime ID, forum topic numbers 

   ```bash
   https://myanimelist.net/forum/?animeid={anime_id}&topic=episode
   ```

   > Configure this using the user input --> API 
   >
   > use web crawler ? 
   >
   > ![image-20230216185515870](C:\Users\jenny\Documents\Typora Images\image-20230216185515870.png)
   >
   > The topic IDs for episodes are all available here
   >
   > ```bash
   > https://api.myanimelist.net/v2/forum/topic/{topic_id}  
   > # plug in the topic ids with a for loop (?)
   > ```
   >
   > Add the topic IDs to a list and loop through all of it (dictionary per episode)

3. access all those forums using this endpoint

   ```bash
   curl 'https://api.myanimelist.net/v2/forum/topic/TOPIC_ID' \
   -H 'Authorization: Bearer YOUR_TOKEN'
   ```

4. Save the comments csv file

5. Need to clean up unnecessary text on the comment  

   1. cleaning done, need proper adjustments 

6. sentimental analysis using nltk

   ```
   from nltk.sentiment.vader import SentimentIntensityAnalyzer
   ```

   unreliable results, need more adjusting for the future 

7. 

Popular --> need sample sizes ?   things to take into considerations 

- statistics 
- random options etc 



1. Evaluate the results: Once you have performed sentiment analysis on the movie reviews, you can evaluate the results by analyzing the distribution of sentiment scores or by comparing the sentiment scores with other metrics such as ratings or box office performance. You can also use various visualization techniques such as scatter plots or bar charts to visualize the sentiment scores.





#### **check** 

gathering forum id

getting the content of the  forum

cleaning text

sentimental analysis

visualization 



Per episode --> ? 





--> some of the user comments had no context of viewed any of their feelings for that episode 

--> MAL API can only have limits to 100 comments per forum post





when offset reaches the value to the point where the value is NULL, then stop the loop 



--> 

-> scale the data --> first and last episodes usually have way more comments than the middle 

overall idea? - scale data and rate the episodes 

but how to scale? 

![image-20230228193439932](C:\Users\jenny\Documents\Typora Images\image-20230228193439932.png)

Relational database set as forum_id references the anime_id 

```json
{'id': 8247, 'title': 'Bleach Movie 4: Jigoku-hen', 'main_picture': {'medium': 'https://api-cdn.myanimelist.net/images/anime/9/26792.jpg', 'large': 'https://api-cdn.myanimelist.net/images/anime/9/26792l.jpg'}, 'start_date': '2010-12-04', 'genres': [{'id': 1, 'name': 'Action'}, {'id': 2, 'name': 'Adventure'}, {'id': 10, 'name': 'Fantasy'}, {'id': 27, 'name': 'Shounen'}], 'mean': 7.61}
```

```
{
    "token_type": "Bearer",
    "expires_in": 2419200,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIn0.eyJhdWQiOiI3YzIzYWNjOTY0YTI3MDAzYWU5ZTJjODBlMmFiNGMwOCIsImp0aSI6IjJmMGM2ZTRmNGIzNmZiNzVlZjRiYWMxNWQ3MGI4MzRlODE4NzI0ODg5MmVhOGQzNTBiZDIwOWQzNTVmZjk1NjQ3NmJiZDhiOGM4ZDFmMWIwIiwiaWF0IjoxNjc2MTA5NjA2LCJuYmYiOjE2NzYxMDk2MDYsImV4cCI6MTY3ODUyODgwNiwic3ViIjoiMjEwODE5OSIsInNjb3BlcyI6W119.fKRkj-BDika--WePFqrQ-gIlMkrWJI1dclSziZouUBWJnfldwuq7exD3c52LdVIJfUP9NzHc-oPwF3G3tBWPtLSNmaXmfxYBTcKYVCja2Y72Cj-XihhPBjiWle2cadISTnDuloZPLuHVEjwThnBL7WvjzeDApoG5Nt9NqO8we83Zztq3tfl0Wu1qG4godMCToMV3b-3D0M9v54e1tZEJT-i0WhDYRTN4UlAG-AVIcPqJLscpKGx_YR1KZX28oPZB6zVVxEbaK7TzMQ751xwKSrrUZDsKYGxu7ixOBMFMInDJ_PPPcwchDE1u76egEHBU1XfwrZErlR6LVHtK16i00A",
    "refresh_token": "def50200e9c09900d812486bbacfa91d6b075d3491a0e063a7cbe7648106a53288444c9573997f7ae2e3cc639d7de9c5060162b3693b8927a0eb90a0a65b97b3cf383f948da162d1c930e5bab0e1d9cc8374abbd0f883ab85e4256ccf837664a6741c5aa080ce7546353fb52b5b03ad503a6c2f85cd052cf1311133b5c33a74581a9588260dc9a921050ff11686ca3ca17d74f1b2f3bb5296389183ba885a4251635432ee20826058c0c1f4b8ec8f59eb302c07bcb08ce875f505e1df89577af7ceb7646c025f4b8730dd848a27339bf0a9f2c6fed238f4256e1ed2f1efde08e5fa8298356d046478b44e89a31230d15372859d01fc8434e915f0b6000c63ed27ff6632e09d6eca2e5ca88f109fa93da8ea67e73463d47f1d083c975f83b9982e2d7b48f1807ea8528e03c233b0b856af9b56a0bd1e299a551d803cdeb1b7cf51bf81026a4c038fa1ff41c965f2aa7816b1c4d1289f56ca2b682c167e22fef864c3323f5ad43ccbc7f10810cf35662ddd0b7be53e8baf3175527498ed8d053b59e40c77f6b27a7df"
}
```

test
