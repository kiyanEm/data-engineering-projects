#خواندن داده-------------------------------------
# وارد کردن کتابخونه pandas
import pandas as pd

# خواندن فایل
df = pd.read_csv('titanic.csv')

# دیدن ۵ ردیف اول
print(df.head())

# اطلاعات کلی
print(df.info())

#تحلیل داده------------------------------------
# شمارش
print(df['Survived'].value_counts())

# میانگین سن
print(df['Age'].mean())

# کمترین و بیشترین
print(df['Age'].min())
print(df['Age'].max())

# گروه‌بندی بر اساس جنسیت
print(df.groupby('Sex')['Survived'].mean())

# گروه‌بندی بر اساس کلاس بلیط
print(df.groupby('Pclass')['Survived'].mean())

# شمارش خالی‌ها
print(df.isnull().sum())

#تمیز کاری------------------------------------

# پر کردن Age خالی با میانگین
df['Age'] = df['Age'].fillna(df['Age'].mean())

# حذف ستون Cabin
df = df.drop(columns=['Cabin'])

# پر کردن Embarked با شایع‌ترین مقدار
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# ذخیره کردن
df.to_csv('titanic_clean.csv', index=False)

#ذخیره در دیتا بیس----------------------------

# اتصال به دیتابیس
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:پسورد@localhost:5432/stor_db')

# ذخیره در دیتابیس
df.to_sql('titanic', engine, if_exists='replace', index=False)

#مرحله ۵ — کوئری SQL در pgAdmin-----------------

#-- همه داده‌ها
SELECT * FROM titanic LIMIT 5;

#-- شمارش نجات‌یافتگان
SELECT "Survived", COUNT(*) FROM titanic GROUP BY "Survived";

#-- نرخ نجات هر جنسیت
SELECT "Sex", AVG("Survived") FROM titanic GROUP BY "Sex";

#-- نرخ نجات هر کلاس
SELECT "Pclass", AVG("Survived") FROM titanic GROUP BY "Pclass";



































































import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X_train, y_train):
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)

    def euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict(self, X_test):
        X_test = np.array(X_test)
        predictions = [self._predict_single(x) for x in X_test]
        return np.array(predictions)

    def _predict_single(self, x):
        # محاسبه فاصله x از تمام نمونه‌های آموزشی
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]

        # پیدا کردن k همسایه‌ی نزدیک (k اندیس با کمترین فاصله)
        k_indices = np.argsort(distances)[:self.k]

        # برچسب k همسایه نزدیک
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        # رأی‌گیری اکثریت
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]


# مثال استفاده
X_train = [[1, 2], [2, 3], [3, 3], [6, 5], [7, 7], [8, 6]]
y_train = [0, 0, 0, 1, 1, 1]

model = KNN(k=3)
model.fit(X_train, y_train)
print(model.predict([[3, 4]]))   # خروجی: [0]