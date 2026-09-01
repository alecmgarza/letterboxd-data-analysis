import sqlite3
import pandas as pd

conn = sqlite3.connect('data/letterboxd.db')

query = '''
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

df = pd.read_sql(query, conn)
print(df.head())

conn.close()