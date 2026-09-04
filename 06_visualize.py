import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

conn = sqlite3.connect('data/letterboxd.db')

query_decades = '''
SELECT
    (m.year / 10) * 10 AS decade,
    COUNT(*) AS total_movies,
    AVG(d.Rating * 2.0) AS avg_my_rating,
    AVG(m.vote_average) AS avg_tmdb_rating,
    AVG((d.Rating * 2.0) - m.vote_average) AS avg_diff
FROM movies_metadata AS m
INNER JOIN diary AS d
ON m.name = d.Name
AND m.year = d.Year
WHERE d.Rating IS NOT NULL 
AND vote_count >= 100
GROUP BY decade
HAVING COUNT(*) >= 3
ORDER BY decade ASC
'''

df_decades = pd.read_sql(query_decades, conn)
df_decades = df_decades.round(2)
print('--- DECADE BREAKDOWN ---\n')
print(df_decades.to_string(index=False), '\n')

df_melted = pd.melt(
    df_decades, 
    id_vars=['decade'], 
    value_vars=['avg_my_rating', 'avg_tmdb_rating'], 
    value_name='rating',
    var_name='source')

df_melted['source'] = df_melted['source'].map({
    'avg_my_rating': 'My Rating',
    'avg_tmdb_rating': 'TMDB Rating'
})

sb.set_theme(style='darkgrid')
plt.figure(figsize=(12,6), dpi=100)

decades_plot = sb.barplot(x='decade', y='rating', hue='source', data=df_melted)

plt.xlabel('Decade', fontsize='12')
plt.ylabel('Average Rating (10-Point Scale)', fontsize='12')
plt.title('My Ratings vs. TMDB Consensus by Decade', fontsize='14')
plt.legend(title='')
plt.ylim(0,10)
plt.tight_layout()
plt.savefig('images/decade_ratings.png')
plt.show()

conn.close()