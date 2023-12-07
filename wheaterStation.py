import mysql.connector
import urllib.request
import xml.etree.ElementTree as ET

# Dodać try catch
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="secret-password",
  database="sys"
)

createTableQuerry = """CREATE TABLE IF NOT EXISTS POGODA_W_POLSCE (
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

mycursor = mydb.cursor()
mycursor.execute(createTableQuerry)

# Dodać try catch
xmlpath = "https://danepubliczne.imgw.pl/api/data/synop/format/xml"
xmlurl= urllib.request.urlopen(xmlpath)
xml_as_string = xmlurl.read()

tree = ET.fromstring(xml_as_string)
items = tree.findall("item")

for item in items:
  id_stacji = item.find("id_stacji").text
  stacja = item.find("stacja").text
  data_pomiaru = item.find("data_pomiaru").text
  godzina_pomiaru = item.find("godzina_pomiaru").text
  temperatura = item.find("temperatura").text
  predkosc_wiatru = item.find("predkosc_wiatru").text
  kierunek_wiatru = item.find("kierunek_wiatru").text
  wilgotnosc_wzgledna = item.find("wilgotnosc_wzgledna").text 
  suma_opadu = item.find("suma_opadu").text
  cisnienie = item.find("cisnienie").text
  if(cisnienie):
    roznica_cisnien = 1013.25-float(cisnienie)
  else:
    roznica_cisnien = None

  wheater_records = """INSERT INTO POGODA_W_POLSCE (
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

  mycursor.execute(wheater_records,(id_stacji, stacja, data_pomiaru, godzina_pomiaru, temperatura, predkosc_wiatru,kierunek_wiatru, wilgotnosc_wzgledna, suma_opadu, cisnienie, roznica_cisnien))
mydb.commit()