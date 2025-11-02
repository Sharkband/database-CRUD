import psycopg2
from psycopg2 import errors

#connecting to postgres
database_connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="###",# put your password to your database
    port=5432
)

#setting connections for executing queries
database_connection.autocommit = True
cursor = database_connection.cursor()

#creating database if one exists
try:
    cursor.execute("CREATE DATABASE university;")
    print("Database created successfully!")
except errors.DuplicateDatabase:
    print("Database already exists")
    cursor.execute("DROP DATABASE university;")
    cursor.execute("CREATE DATABASE university;")
    print("Database created successfully!")

#closing connections
cursor.close()
database_connection.close()
 