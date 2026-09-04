
import pandas as pd

df = pd.read_csv('netflix.csv')
print(df.head())

print(df.info())

print(df.isnull().sum())

df['ratinglevel'] = df['ratinglevel'].fillna('This movie has not been rated.')

df = df.dropna(subset=['user_rating_score'])

df.to_csv('netflix_clean.csv', index=False)

from sqlalchemy import create_engine

# اتصال به PostgreSQL
engine = create_engine('postgresql://postgres:33755975@localhost:5432/stor_db')

# ریختن داده تایتانیک توی دیتابیس
df.to_sql('netflix', engine, if_exists='replace', index=False)
print('داده نتفیلیکس توی دیتابیس ذخیره شد!')


