import pandas as pd

df = pd.read_csv('data/diary.csv')

print(df.head(10))

print(df.info())

total_movies = len(df)
print(f"Total Movies Logged: {total_movies}")

max_rating = df['Rating'].max()
print(f"Max Rating: {max_rating}")

min_rating = df['Rating'].min()
print(f"Min Rating: {min_rating}")

avg_rating = df['Rating'].mean().round(2)
print(f"Average Rating: {avg_rating}")

df['Decade'] = df['Year'] // 10 * 10
print(df.groupby('Decade')['Rating'].mean().round(2))