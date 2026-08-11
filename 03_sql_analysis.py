import pandas as pd
import sqlite3

conn = sqlite3.connect('data/letterboxd.db')

query = '''
SELECT
    CASE
        WHEN Rewatch IS NULL THEN 'First Watch'
        ELSE 'Rewatch'
    END AS watch_type,
    COUNT(*) AS total_movies,
    ROUND(AVG(Rating), 2) AS avg_rating
FROM diary
GROUP BY watch_type;
'''

df = pd.read_sql(query, conn)
print(df)

conn.close()