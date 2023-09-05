from mysql.connector import connect, Error

try:
    with connect(
            host="localhost",
            user='',
            password='',
            database="products",
    ) as connection:
        create_table_query = """
        CREATE TABLE products(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            url VARCHAR(200),
            price INT,
            discount INT
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
except Error as e:
    print(e)
