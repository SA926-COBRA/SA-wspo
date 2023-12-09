# Tworzenie tabeli, jeśli nie istnieje
def createTableQuery(): 
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
    return createTableQuery

#  Wstawienie rekordu do bazy danych z pominięciem duplikatów
def insertQuery():
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

    return insertQuery
