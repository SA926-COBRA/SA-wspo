# Import niezbędnych bibliotek
from dotenv import load_dotenv
import mysql.connector
import os
import urllib.request
import xml.etree.ElementTree as ET

# Import funkcji z innych plików
from sqlQueries import *

class DatabaseConfig:
    def __init__(self):
        # Wczytanie zmienne środowiskowe z pliku .env
        load_dotenv()

        # Przypisanie wartości do atrybutów
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_DATABASE = os.getenv("DB_DATABASE")

# Utworzenie instancji klasy
db_config = DatabaseConfig()

# IMPLEMENTACJA KLASY - DO POPRAWY I ZASTOSOWANIA W KODZIE
class WeatherMeasurement:
    def __init__(self, measurement):
        self.id_stacji = measurement.find("id_stacji").text
        self.stacja = measurement.find("stacja").text
        self.data_pomiaru = measurement.find("data_pomiaru").text
        self.godzina_pomiaru = measurement.find("godzina_pomiaru").text
        self.temperatura = measurement.find("temperatura").text
        self.predkosc_wiatru = measurement.find("predkosc_wiatru").text
        self.kierunek_wiatru = measurement.find("kierunek_wiatru").text
        self.wilgotnosc_wzgledna = measurement.find("wilgotnosc_wzgledna").text
        self.suma_opadu = measurement.find("suma_opadu").text
        self.cisnienie = measurement.find("cisnienie").text

# Przypisanie linku API do zmiennej
apiUrl = "https://danepubliczne.imgw.pl/api/data/synop/format/xml"

# Pobieranie i parsowanie danych z API
def getAndParseXmlData(apiUrl):
    xmlUrl = urllib.request.urlopen(apiUrl)
    xmlAsString = xmlUrl.read()
    xmlTree = ET.fromstring(xmlAsString)
    foundMeasurement = xmlTree.findall("item")
   
    # Przekształcanie znalezionych pomiarów na obiekty
    foundMeasurementObjects = [WeatherMeasurement(measurement) for measurement in foundMeasurement]

    # return foundMeasurementObjects
    return foundMeasurement

# Blok try-except mający na celu zapobieganie całkowitego zatrzymania się programu i wyświetleniu komunikatów w przypadku wystąpienia błędów
try:
    # Połączenie z bazą danych
    db = mysql.connector.connect(
        host=db_config.DB_HOST,
        user=db_config.DB_USER,
        password=db_config.DB_PASSWORD,
        database=db_config.DB_DATABASE
    )

    # Utworzenie kursora w celu połączenia i wykonywania poleceń na bazie danych
    cursor = db.cursor()
    # Wykonanie zapytania ze zmiennej createTableQuery
    cursor.execute(createTableQuery())
    # Wywołanie funkcji i przypisanie zwróconej wartości do zmiennej
    foundMeasurement = getAndParseXmlData(apiUrl)

    # Dodawanie rekordów ze sparsowanego XML
    for measurement in foundMeasurement:
        try:
            id_stacji = measurement.find("id_stacji").text
            stacja = measurement.find("stacja").text
            data_pomiaru = measurement.find("data_pomiaru").text
            godzina_pomiaru = measurement.find("godzina_pomiaru").text
            temperatura = measurement.find("temperatura").text
            predkosc_wiatru = measurement.find("predkosc_wiatru").text
            kierunek_wiatru = measurement.find("kierunek_wiatru").text
            wilgotnosc_wzgledna = measurement.find("wilgotnosc_wzgledna").text
            suma_opadu = measurement.find("suma_opadu").text
            cisnienie = measurement.find("cisnienie").text

            # Wyliczanie od różnicy ciśnienia wzorcowego tylko jeśli pole cisnienie nie przyjmuje wartości NULL
            if cisnienie:
                roznica_cisnien = 1013.25 - float(cisnienie)
            else:
                roznica_cisnien = None

            # Wykonanie polecenia ze zmiennej insertQuery
            cursor.execute(insertQuery(), (
                id_stacji, stacja, data_pomiaru, godzina_pomiaru, temperatura, predkosc_wiatru, kierunek_wiatru,
                wilgotnosc_wzgledna, suma_opadu, cisnienie, roznica_cisnien))
            
        # Błąd podczas dodawania rekordu do tabeli
        except Exception as e:
            print(f"Błąd podczas przetwarzania rekordu: {e}")

    # Zatwierdzenie zmian w bazie danych
    db.commit()

# Błąd związany z biblioteką mysql.connector - na przykład błąd połączenia z bazą danych
except mysql.connector.Error as err:
    print(f"Błąd MySQL: {err}")
# Błąd niezwiązany z biblioteką mysql.connector - na przykład przy próbie dopisania rekordów do nieistniejącej tabeli
except Exception as e:
    print(f"Wystąpił błąd: {e}")
# Zamknięcie połączenia z bazą danych
finally:
    if db.is_connected():
        cursor.close()
        db.close()
