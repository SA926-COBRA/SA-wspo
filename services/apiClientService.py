import os
import urllib.request
import xml.etree.ElementTree as ET

# Pobieranie i parsowanie danych z API
def getAndParseXmlData(path):

    # Blok try-except mający na celu zapobieganie całkowitego zatrzymania się serwisu i wyświetleniu komunikatów w przypadku wystąpienia błędów
    try:
        xmlUrl = urllib.request.urlopen(os.getenv("API_URL") + path)

        # Sprawdzanie czy API zwraca status code 200
        if xmlUrl.getcode() == 200:
            xmlAsString = xmlUrl.read()
            xmlTree = ET.fromstring(xmlAsString)
            foundMeasurement = xmlTree.findall("item")
        else:
            print(f'Błąd: API zwróciło status code {xmlUrl.getcode()}')

    # Błąd związany z API - na przykład w przypadku braku odpowiedzi z API
    except Exception as error:
        print(f"Wystąpił błąd API: {error}")

    return foundMeasurement