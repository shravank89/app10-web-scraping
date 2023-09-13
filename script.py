import sqlite3

# This can be used to recreate the database for testing purposes

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE events(name, city, date)")

connection.commit()