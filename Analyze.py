import pandas as pd

df = pd.read_csv('train.csv')

print(df.head())
print(df.info())

# چند نفر نجات پیدا کردن؟
print(df['Survived'].value_counts())

# میانگین سن مسافرها چقدر بوده؟
print(df['Age'].mean())

# نسبت نجات زن‌ها در مقایسه با مردها
print(df.groupby('Sex')['Survived'].mean())

# آیا کلاس بلیط روی شانس نجات تاثیر داشته؟
print(df.groupby('Pclass')['Survived'].mean())

# جوون‌ترین و مسن‌ترین مسافر
print('جوون‌ترین:', df['Age'].min())
print('مسن‌ترین:', df['Age'].max())

# ببینیم کجاها داده خالی داریم
print(df.isnull().sum())

# Age: خالی‌ها رو با میانگین سن پر کن
df['Age'] = df['Age'].fillna(df['Age'].mean())

# Cabin: خیلی ناقصه، کلاً حذفش می‌کنیم
df = df.drop(columns=['Cabin'])

# Embarked: فقط 2 تاست، با شایع‌ترین مقدار پر کن
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# حالا دوباره چک کن
print(df.isnull().sum())

# ذخیره داده تمیز
df.to_csv('titanic_clean.csv', index=False)
print('فایل ذخیره شد!')

# ---- مرحله 4: SQL ----

import sqlite3

# دیتا رو بریز توی یه دیتابیس موقت
conn = sqlite3.connect(':memory:')
df.to_sql('titanic', conn, index=False)

# اولین کوئری SQL
result = conn.execute("SELECT * FROM titanic LIMIT 5")
for row in result:
    print(row)


from sqlalchemy import create_engine

# اتصال به PostgreSQL
engine = create_engine('postgresql://postgres:33755975@localhost:5432/stor_db')

# ریختن داده تایتانیک توی دیتابیس
df.to_sql('titanic', engine, if_exists='replace', index=False)
print('داده تایتانیک توی دیتابیس ذخیره شد!')