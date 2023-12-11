import mysql.connector
import os

def getDataBaseInstance():

    # Blok try-except mający na celu zapobieganie całkowitego zatrzymania się serwisu i wyświetleniu komunikatów w przypadku wystąpienia błędów
    try:
        dbInstance = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_DATABASE")
        )

    # Błąd związany z biblioteką mysql.connector - na przykład błąd połączenia z bazą danych
    except mysql.connector.Error as error:
        print(f"Błąd MySQL: {error}")

    return dbInstance