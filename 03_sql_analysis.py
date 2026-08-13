import pandas as pd
import sqlite3

conn = sqlite3.connect('data/letterboxd.db')

query_1 = '''
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

df = pd.read_sql(query_1, conn)
print('\n--- QUERY 1: FIRST WATCH VS. REWATCH ---\n')
print(df)
print('\n')

query_2 = '''
SELECT
    "Watched Date" AS watched_date,
    Name AS film_name,
    Rating AS rating,
    ROUND(AVG(Rating) OVER (
        ORDER BY "Watched Date"
        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_avg
FROM diary;
'''

df_rolling = pd.read_sql(query_2, conn)
print('--- QUERY 2: ROLLING 10-MOVIE AVERAGE ---\n')
print(df_rolling.head(15))

conn.close()