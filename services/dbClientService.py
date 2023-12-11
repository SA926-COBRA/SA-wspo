import mysql.connector
import os

def getDataBaseInstance():
    dbInstance = None

    try:
        dbInstance = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
    except mysql.connector.Error as err:
        print(f"Błąd MySQL: {err}")

    # Błąd związany z biblioteką mysql.connector - na przykład błąd połączenia z bazą danych
    return dbInstance