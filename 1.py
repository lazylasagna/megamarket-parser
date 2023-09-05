from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user='',
        password='',
    ) as connection:
        create_db_query = "CREATE DATABASE products"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)
