import pandas as pd
import sqlite3

df = pd.read_csv('data/diary.csv')
df['Decade'] = df['Year'] // 10 * 10

conn = sqlite3.connect('data/letterboxd.db')

df.to_sql(name="diary", if_exists="replace", index=False, con=conn)

conn.close()