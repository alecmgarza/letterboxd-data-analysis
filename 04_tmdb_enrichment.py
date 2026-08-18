import pandas as pd
import sqlite3
import os
import requests
from dotenv import load_dotenv


conn = sqlite3.connect('data/letterboxd.db')

query = '''
SELECT DISTINCT Name, Year
FROM diary
WHERE Name IS NOT NULL;
'''

df = pd.read_sql(query, conn)
print(df.head(15).to_string(index=False))

enriched_data = []

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

for row in df.head(15).itertuples():
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': api_key,
        'query': row.Name,
        'year': row.Year
    }
    r = requests.get(url, params=params)
    print(r.status_code, row.Name)