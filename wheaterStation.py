import mysql.connector
import urllib.request
import xml.etree.ElementTree as ET

try:
    # Połączenie z bazą danych
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="secret-password",
        database="sys"
    )

    # Tworzenie tabeli, jeśli nie istnieje
    createTableQuery = """CREATE TABLE IF NOT EXISTS POGODA_W_POLSCE (
      id INT unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
      id_stacji INT,
      stacja VARCHAR(255),
      data_pomiaru DATE,
      godzina_pomiaru TIME,
      temperatura FLOAT,
      predkosc_wiatru INT,
      kierunek_wiatru INT,
      wilgotnosc_wzgledna FLOAT,
      suma_opadu FLOAT,
      cisnienie FLOAT,
      roznica_cisnien FLOAT
    );"""

    cursor = db.cursor()
    cursor.execute(createTableQuery)

    # Pobieranie danych z API i parsowanie XML
    xmlPath = "https://danepubliczne.imgw.pl/api/data/synop/format/xml"
    xmlUrl = urllib.request.urlopen(xmlPath)
    xmlAsString = xmlUrl.read()
    xmlTree = ET.fromstring(xmlAsString)
    foundMeasurement = xmlTree.findall("item")

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

            if cisnienie:
                roznica_cisnien = 1013.25 - float(cisnienie)
            else:
                roznica_cisnien = None

            # Wstawianie rekordu do bazy danych
            recordToInsert = """INSERT INTO POGODA_W_POLSCE (
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
                roznica_cisnien) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )"""

            cursor.execute(recordToInsert, (
                id_stacji, stacja, data_pomiaru, godzina_pomiaru, temperatura, predkosc_wiatru, kierunek_wiatru,
                wilgotnosc_wzgledna, suma_opadu, cisnienie, roznica_cisnien))
        except Exception as e:
            print(f"Błąd podczas przetwarzania rekordu: {e}")

    # Zatwierdzenie zmian w bazie danych
    db.commit()

except mysql.connector.Error as err:
    print(f"Błąd MySQL: {err}")
except Exception as e:
    print(f"Wystąpił błąd: {e}")
finally:
    # Zamknięcie połączenia z bazą danych
    if db.is_connected():
        cursor.close()
        db.close()
