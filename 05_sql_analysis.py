import sqlite3
import pandas as pd

conn = sqlite3.connect('data/letterboxd.db')

query_1 = '''
SELECT
    COUNT(*) AS total_movies, 
    SUM(m.runtime) AS total_min, 
    ROUND(SUM(m.runtime) / 60.0, 1) AS total_hr,
    ROUND(SUM(m.runtime) / (60.0 * 24.0), 2) AS total_days,
    ROUND(AVG(m.runtime), 1) AS avg_runtime
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year;
'''

df_runtime = pd.read_sql(query_1, conn)
print(df_runtime.head(), '\n')

query_2 = '''
SELECT
    m.name AS name,
    m.year AS year,
    d.Rating AS my_rating,
    m.vote_average AS tmdb_rating,
    ROUND((d.Rating * 2.0) - m.vote_average, 2) AS rating_diff
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year
WHERE d.Rating IS NOT NULL AND vote_count >= 100
ORDER BY rating_diff ASC
'''

df_overrated = pd.read_sql(query_2, conn)
print(df_overrated.head(), '\n')

query_3 = '''
SELECT
    m.name AS name,
    m.year AS year,
    d.Rating AS my_rating,
    m.vote_average AS tmdb_rating,
    ROUND((d.Rating * 2.0) - m.vote_average, 2) AS rating_diff
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year
WHERE d.Rating IS NOT NULL AND vote_count >=100
ORDER BY rating_diff DESC
'''

df_underrated = pd.read_sql(query_3, conn)
print(df_underrated.head(), '\n')

conn.close()