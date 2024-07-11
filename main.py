import requests
import psycopg2

url = "https://dummyjson.com/products"
response = requests.get(url)
data = response.json()

conn = psycopg2.connect(
    dbname="mydb",
    user="postgres",
    password="0707",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE products (
    id                     SERIAL PRIMARY KEY,
    title                  TEXT,
    description            TEXT,
    price                  REAL,
    discountPercentage     REAL,
    rating                 REAL,
    stock                  INTEGER,
    brand                  TEXT,
    category               TEXT,
    thumbnail              TEXT,
    weight                 REAL
)
''')
conn.commit()

products = data['products']
for product in products:
    title = product.get('title')
    description = product.get('description')
    price = product.get('price')
    discountPercentage = product.get('discountPercentage')
    rating = product.get('rating')
    stock = product.get('stock')
    brand = product.get('brand')
    category = product.get('category')
    thumbnail = product.get('thumbnail')
    weight = product.get('weight')

    cursor.execute('''
    INSERT INTO products (title,
    description,
    price,
    discountPercentage,
    rating,
    stock,
    brand,
    category,
    thumbnail,
    weight)
    VALUES (%s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s)
    ''',
                   (title, description, price, discountPercentage, rating, stock, brand, category, thumbnail, weight))
conn.commit()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
