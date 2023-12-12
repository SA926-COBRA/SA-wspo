# Zadanie praktyczne - Bartosz Kulpa

Zadanie praktyczne na stanowisko IT Systems Integration Specialist.

## Koncepcja działania programu

Celem programu jest zasilenie tabeli `POGODA_W_POLSCE` danymi dotyczącymi pomiarów pogodowych udostępnianych przez Instytut Meteorologii i Gospodarki Wodnej (IMGW). Program został przygotowany w języku Python z wykorzystaniem zapytań MySQL.</br>
</br>
W momencie wywołania program komunikuje się z API IMGW, pobiera dane pochodzące z chwili wywołania, dokonuje odpowiedniej obróbki, a następnie zasila bazę danych. Testy działania programu zostały wykonane na bazie danych MySQL w środowisku Docker.

## Wykonanie programu

W celu wykonania programu należy uruchomić plik `createAndPopulateWeatherMeasurement.py`.

## Instalacja niezbędnych bibliotek

W celu instalacji niezbędnych bibliotek należy użyć polecenia:

```shell
pip install -r requirements.txt

```

lub opcjonalnie

```shell
pip3 install -r requirements.txt

```

## Zmienne środowiskowe

W celu konfiguracji połączenia z bazą danych należy:

- Skopiować plik `.env.example` i zapisać jako `.env`.
- Ustawić odpowiednie dane dostępowe do bazy danych.

## Sposób cyklicznego pobierania danych z API do bazy danych

W celu pobierania i zasilania bazy danych danymi w sposób cykliczny wykorzystał bym technologie AWS Lambda i EventBridge jako Scheduler.
W celu implementacji wymienionych rozwiązań do przesłanego programu utworzyłbym dodatkowy serwis, którego zadaniem byłoby pobieranie danych z API i zapisanie ich do bazy danych.
Serwis zawierałby trigger mający na celu cykliczne uruchomienie Schedulera wywołujący Lambdę według ustalonego harmonogramu (na przykład co 4 godziny).
