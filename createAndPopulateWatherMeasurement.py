# Import niezbędnych bibliotek
from dotenv import load_dotenv
import services.apiClientService as apiClientService
import services.dbClientService as dbClientService

# Wczytanie danych dostępowych do bazy danych z pliku .env
load_dotenv()

# Zapisanie sparsowanych danych z API do listy
def parseMeasurement(measurement):
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
        roznica_cisnien = 1013.25 - float(cisnienie) if cisnienie else None

        return [
            id_stacji,
            stacja,
            data_pomiaru,
            godzina_pomiaru,
            temperatura,
            predkosc_wiatru,
            kierunek_wiatru,
            wilgotnosc_wzgledna,
            suma_opadu,
            cisnienie,
            roznica_cisnien
        ]

# Tworzenie tabeli, jeśli nie istnieje
createTableQuery = """CREATE TABLE IF NOT EXISTS POGODA_W_POLSCE (
    id INT unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_stacji INT,
    stacja VARCHAR(255),
    data_pomiaru DATE,
    godzina_pomiaru VARCHAR(10),
    temperatura FLOAT,
    predkosc_wiatru FLOAT,
    kierunek_wiatru INT,
    wilgotnosc_wzgledna FLOAT,
    suma_opadu FLOAT,
    cisnienie FLOAT,
    roznica_cisnien FLOAT
);"""

#  Wstawienie rekordu do bazy danych (z pominięciem duplikatów)
insertQuery = """INSERT INTO POGODA_W_POLSCE (
    id_stacji,
    stacja, 
    data_pomiaru,
    godzina_pomiaru,
    temperatura,
    predkosc_wiatru,
    kierunek_wiatru,
    wilgotnosc_wzgledna, 
    suma_opadu,
    cisnienie,
    roznica_cisnien
) SELECT * FROM (
    SELECT 
    %s as id_stacji,
    %s as stacja,
    %s as data_pomiaru,
    %s as godzina_pomiaru,
    %s as temperatura,
    %s as predkosc_wiatru,
    %s as kierunek_wiatru,
    %s as wilgotnosc_wzgledna,
    %s as suma_opadu,
    %s as cisnienie,
    %s as roznica_cisnien
) AS tmp WHERE NOT EXISTS (
    SELECT * 
    FROM POGODA_W_POLSCE 
    WHERE 
        id_stacji = tmp.id_stacji AND
        data_pomiaru = tmp.data_pomiaru AND
        godzina_pomiaru = tmp.godzina_pomiaru
);"""

# Utworzenie instancji bazy danych
db = dbClientService.getDataBaseInstance()

# Blok try-except mający na celu zapobieganie całkowitego zatrzymania się programu i wyświetleniu komunikatów w przypadku wystąpienia błędów
try:

    # Utworzenie kursora w celu połączenia i wykonywania poleceń na bazie danych
    cursor = db.cursor()

    # Wykonanie zapytania ze zmiennej createTableQuery
    cursor.execute(createTableQuery)

    # Wywołanie funkcji i przypisanie zwróconej wartości do zmiennej
    foundMeasurement = apiClientService.getAndParseXmlData("/data/synop/format/xml")

    # Dodawanie rekordów ze sparsowanego XML
    for measurement in foundMeasurement:
        try:
            parsedMeasurement = parseMeasurement(measurement)

            # Wykonanie polecenia ze zmiennej insertQuery
            cursor.execute(insertQuery, parsedMeasurement)            

        # Błąd podczas dodawania rekordu do tabeli
        except Exception as error:
            print(f"Błąd podczas przetwarzania rekordu: {error}")

    # Zatwierdzenie zmian w bazie danych
    db.commit()

# Błąd niezwiązany z biblioteką mysql.connector - na przykład przy próbie dopisania rekordów do nieistniejącej tabeli
except Exception as error:
    print(f"Wystąpił błąd: {error}")

# Zamknięcie połączenia z bazą danych
finally:
    if db.is_connected():
        cursor.close()
        db.close()