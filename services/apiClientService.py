import os
import urllib.request
import xml.etree.ElementTree as ET

# Pobieranie i parsowanie danych z API
def getAndParseXmlData(path):
    try:
        xmlUrl = urllib.request.urlopen(os.getenv("API_URL") + path)

        xmlAsString = xmlUrl.read()
        xmlTree = ET.fromstring(xmlAsString)
        foundMeasurement = xmlTree.findall("item")

    except Exception as e:
        print(f"Wystąpił błąd API: {e}")

    return foundMeasurement