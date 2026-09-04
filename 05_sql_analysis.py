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
print('--- OVERALL RUNTIME METRICS ---\n')
print(df_runtime.head().to_string(index=False), '\n')

query_2 = '''
SELECT
    m.name AS name,
    m.year AS year,
    (d.Rating * 2.0) AS my_rating,
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
df_overrated = df_overrated.round(2)
print('--- TOP 5 OVERRATED by TMDB ---\n')
print(df_overrated.head(5).to_string(index=False), '\n')

query_3 = '''
SELECT
    m.name AS name,
    m.year AS year,
    (d.Rating * 2.0) AS my_rating,
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
df_underrated = df_underrated.round(2)
print('--- TOP 5 UNDERRATED by TMDB ---\n')
print(df_underrated.head(5).to_string(index=False), '\n')

query_4 = '''
SELECT
    m.genres AS genres,
    (d.Rating * 2.0) AS my_rating,
    m.vote_average AS tmdb_rating,
    d.Rating * 2.0 - m.vote_average AS rating_diff
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year
WHERE d.Rating IS NOT NULL 
AND vote_count >= 100
AND m.genres != ''
'''

df_genres = pd.read_sql(query_4, conn)
df_genres['genres'] = df_genres['genres'].str.split(', ')

df_exploded = df_genres.explode('genres')

genre_summary = df_exploded.groupby('genres').agg(
    total_movies=('my_rating', 'count'),
    avg_my_rating=('my_rating', 'mean'),
    avg_tmdb_rating=('tmdb_rating', 'mean'),
    avg_diff=('rating_diff', 'mean')
).reset_index()

filtered_summary = genre_summary[genre_summary['total_movies'] >= 10]

sorted_summary = filtered_summary.sort_values(by='avg_my_rating', ascending=False)
sorted_summary = sorted_summary.round(2)

print('--- GENRE BREAKDOWN (min. 10 movies) ---\n')
print(sorted_summary.to_string(index=False), '\n')

query_5 = '''
SELECT
    (m.year / 10) * 10 AS decade,
    COUNT(*) AS total_movies,
    AVG((d.Rating) * 2.0) AS avg_my_rating,
    AVG(m.vote_average) AS avg_tmdb_rating,
    AVG((d.Rating * 2.0) - m.vote_average) AS avg_diff
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year
WHERE d.Rating IS NOT NULL 
AND vote_count >= 100
GROUP BY decade
ORDER BY decade ASC
'''

df_decades = pd.read_sql(query_5, conn)
df_decades = df_decades.round(2)
print('--- DECADE BREAKDOWN ---\n')
print(df_decades.to_string(index=False), '\n')

conn.close()