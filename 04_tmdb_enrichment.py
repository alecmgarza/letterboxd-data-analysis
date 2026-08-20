import pandas as pd
import sqlite3
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

conn = sqlite3.connect('data/letterboxd.db')

query = '''
SELECT DISTINCT Name, Year
FROM diary
WHERE Name IS NOT NULL;
'''
df = pd.read_sql(query, conn)

enriched_data = []

for row in df.itertuples():
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': api_key,
        'query': row.Name,
        'year': row.Year
    }
    r = requests.get(url, params=params)
    data = r.json()

    if data.get('results'):
        movie_id = data['results'][0]['id']
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        details_params = {
            'api_key': api_key
        }
        details_r = requests.get(details_url, params=details_params)
        details_data = details_r.json()

        enriched_data.append({
            'name': row.Name,
            'year': row.Year,
            'id': movie_id,
            'runtime': details_data.get('runtime'),
            'vote_average': details_data.get('vote_average'),
            'vote_count': details_data.get('vote_count'),
            'genres': ', '.join([genre['name'] for genre in data.get('genres', [])]),
            'overview': data.get('overview')
        })
        print(f"Enriched: {row.Name}")

    time.sleep(0.05)

df_enriched = pd.DataFrame(enriched_data)
df_enriched.to_sql('movies_metadata', conn, if_exists='replace', index=False)
conn.close()