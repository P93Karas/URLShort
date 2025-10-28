# Django URL Shortener

Prosta aplikacja do skracania URL'i

---

## In-Memory VS DB

Zanim zacząłem działać, przez jakiś czas zastanawiałem się czy wogóle korzystać z bazy danych. W teorii, dla takiej przykładowej aplikacji mógłbym trzymać wszystkie short_url w pamięci, dzieki czemu lookup byłby szybszy niż w przypadku zaglądania do bazy danych.

Ostatecznie jednak stwierdziłem, że zostawie bazowy sqlite. Głównie dlatego że nie musiałem się martwić że moje short url znikną przy zamknięciu apki.

## Generowanie Skróconego URL

By wygenerować skrócony url, wykorzystuje oryginalny url, który hashuje SHA256, a następnie konwertuje na kod alfanumeryczny.

Jestem świadomy że ryzyko "kolizji" w takim przypadku jest małe, ale na wszelki wypadek jeżeli dwa rózne url miałyby ten sam skrócony short url - przed zapisaniem do DB, dodaje uuid4 do wartości salt, żeby zapewnić unikalny short url dla różnych adresów.

## Zapisywanie Short URL

Główna logika znajduje się w metodzie save() modelu ShortURL. Obsługuje tworzenie ale też updatowanie oryginalnego url - wraz z przypisaniem nowego short url.

## Swagger

Po wejściu na "http://127.0.0.1:8000/" automatycznie nastepuje redirect na podstrone swaggera, gdzie łatwo przeklikać się przez funkcjonalności API

- /api/v1/list/ zwraca liste skróconych url (normalnie dodał bym paginacje)
- /api/v1/shorten/ przyjmuje "original_url", i zwraca skróconego url (zwraca full path jak i sam kod)
- /api/v1/unshorten/{short_url}/ dla podanego short_url, zwraca oryginalny url

oprócz endpointów api, jest także widok ShortURLRedirectView(), dzieki któremu po wklejeniu "full short url" zwracanego przy stworzeniu skróconego url - faktycznie nastąpi przekierowanie.

## Testy

Testy napisane w pytest - Jeden end-to-end i osiem jednostkowych sprawdzające funkcjonalności apki

## Setup

Na początku chciałem dodac dockera, ale stwierdziłem że do apki która nawet nie korzysta z postgresql i osobnego frontu - Docker może być overkillem.

Zamiast tego dodałem prosty setup.sh, który tworzy venv, instaluje requirementsy, robi migracje i odpala runserver.

## Odpalenie Projektu

1. git clone https://github.com/P93Karas/URLShort.git

2. cd URLShort

3. chmod +x setup.sh

4. ./setup.sh

5. aplikacja odpala sie na "http://127.0.0.1:8000/"

## Odpalenie testów

1. source venv/bin/activate

2. pytest

---
