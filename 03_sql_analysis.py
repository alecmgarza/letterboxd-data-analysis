import pandas as pd
import sqlite3

conn = sqlite3.connect('data/letterboxd.db')

# QUERY 1: compare first watch ratings against rewatch ratings

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
print(df.to_string(index=False))
print('\n')

# QUERY 2: calculate rolling 10-movie averages

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
print(df_rolling.head(15).to_string(index=False))

# QUERY 3: rank decades by highest average ratings
# (excluding movies with less than 5 movies watched)

query_3 = '''
WITH watch_date_decades AS (
    SELECT 
        Year / 10 * 10 AS decade,
        ROUND(AVG(Rating), 2) AS avg_rating,
        COUNT(*) AS total_movies
    FROM diary
    WHERE Year IS NOT NULL
    GROUP BY decade
)
SELECT
    DENSE_RANK() OVER (ORDER BY avg_rating DESC) AS rank,
    *
FROM watch_date_decades
WHERE total_movies >= 5;
'''

df_decades = pd.read_sql(query_3, conn)
print('\n--- QUERY 3: AVERAGE RATINGS BY DECADE (excl. < 5 movies) ---\n')
print(df_decades.to_string(index=False))

conn.close()