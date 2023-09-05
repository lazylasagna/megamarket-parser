from mysql.connector import connect, Error
try:
    with connect(
            host="localhost",
            user='',
            password='',
            database="products",
    ) as connection:
        select_movies_query = "SELECT * FROM products"
        with connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)
