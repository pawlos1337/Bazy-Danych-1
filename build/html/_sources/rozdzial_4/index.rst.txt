================================================
Rozdział 4: Implementacja fizyczna i zasilanie bazy danych
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Definicja fizyczna bazy danych (Zadanie 1)
==========================================
Na podstawie opracowanych wcześniej modeli logicznych przygotowano skrypty DDL (Data Definition Language) dla dwóch docelowych silników relacyjnych baz danych: PostgreSQL oraz SQLite. Kody te p[...]

Skrypt dla środowiska PostgreSQL
--------------------------------
Środowisko PostgreSQL pozwala na wykorzystanie zaawansowanych, natywnych typów danych oraz rygorystyczne egzekwowanie więzów integralności. W poniższym skrypcie kluczowym elementem jest uży[...]

.. code-block:: sql

    -- Fragment kodu definicji kluczowych tabel (PostgreSQL)
    CREATE TABLE Ksiazki (
        ID_Ksiazki SERIAL PRIMARY KEY,
        ID_Autora INTEGER REFERENCES Autorzy(ID_Autora),
        ID_Kategorii INTEGER REFERENCES Kategorie(ID_Kategorii),
        Tytul VARCHAR(150) NOT NULL,
        Rok_Wydania SMALLINT
    );

    CREATE TABLE Wypozyczenia (
        ID_Wypozyczenia SERIAL PRIMARY KEY,
        ID_Czytelnika INTEGER REFERENCES Czytelnicy(ID_Czytelnika),
        ID_Ksiazki INTEGER REFERENCES Ksiazki(ID_Ksiazki),
        Data_Wypozyczenia DATE DEFAULT CURRENT_DATE,
        Data_Zwrotu DATE
    );

Skrypt dla środowiska SQLite
----------------------------
W silniku SQLite struktura ulega pewnemu uproszczeniu z powodu mniejszej rygorystyczności typowania oraz bardzo ograniczonej liczby wbudowanych klas typów danych (np. brak odrębnego typu daty).[...]

.. code-block:: sql

    -- Fragment kodu definicji kluczowych tabel (SQLite)
    CREATE TABLE Wypozyczenia (
        ID_Wypozyczenia INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Czytelnika INTEGER,
        ID_Ksiazki INTEGER,
        Data_Wypozyczenia TEXT,
        Data_Zwrotu TEXT,
        FOREIGN KEY(ID_Czytelnika) REFERENCES Czytelnicy(ID_Czytelnika),
        FOREIGN KEY(ID_Ksiazki) REFERENCES Ksiazki(ID_Ksiazki)
    );

Mechanizm zasilania bazy danych (Zadanie 2)
===========================================
Posiadając gotową strukturę bazy, należało wyposażyć ją w dane demonstracyjne. Przygotowano zbiór danych testowych, które zostały poddane wsadowemu ładowaniu (batch import).

Formatyzacja danych (Pliki CSV)
-------------------------------
Dane do importu przygotowano w niezależnym formacie płaskim CSV (Comma-Separated Values). Takie podejście pozwala na łatwą edycję danych poza systemem bazodanowym. Poniżej zaprezentowano wy[...]

.. code-block:: text

    Nazwa_Kategorii
    Fantastyka
    Kryminał
    Literatura faktu
    Poezja
    Horror

Implementacja mechanizmu importu
--------------------------------
Do zaimportowania powyższych danych wybrano mechanizm wprowadzania wielowartościowego oparty na technice **INSERT (multi-value/batch)**. Rozwiązanie zrealizowano z wykorzystaniem języka Python[...]

Wybór tego mechanizmu podyktowany jest kompromisem między uniwersalnością a wydajnością. Użycie metody ``executemany()`` na obiekcie kursora bazy danych pozwala na szybkie wstawienie wielu [...]

Poniżej przedstawiono fragment skryptu aplikacyjnego odpowiedzialnego za odczyt z pliku i zasilenie tabel:

.. code-block:: python

    import csv
    import psycopg

    # 1. Wczytywanie danych z pliku CSV do struktury iterowalnej (listy krotek)
    def wczytaj_dane_csv(sciezka_pliku):
        dane = []
        with open(sciezka_pliku, mode='r', encoding='utf-8') as plik:
            csv_reader = csv.reader(plik)
            next(csv_reader)  # Pominięcie wiersza nagłówka
            for wiersz in csv_reader:
                dane.append(tuple(wiersz))
        return dane

    # 2. Właściwy proces wsadowego importu do bazy PostgreSQL
    def importuj_do_postgres(kategorie_do_importu, db_config):
        try:
            # Użycie Context Managera dla bezpiecznego zarządzania transakcjami
            with psycopg.connect(**db_config) as conn:
                with conn.cursor() as cursor:

                    # Definicja sparametryzowanego zapytania zapobiegającego SQL Injection
                    zapytanie_sql = "INSERT INTO Kategorie (Nazwa_Kategorii) VALUES (%s)"

                    # Wsadowe wywołanie zapytań (batch insert)
                    cursor.executemany(zapytanie_sql, kategorie_do_importu)

                    print(f"Pomyślnie zaimportowano {len(kategorie_do_importu)} rekordów.")

        except Exception as e:
            print(f"Wystąpił błąd operacji wsadowej: {e}")

Podsumowanie
============

Niniejszy rozdział wieńczy etap projektowania i wdrażania struktury relacyjnej bazy danych dla systemu zarządzania biblioteką. Poprzez transformację modelu logicznego do postaci fizycznej oraz realizację mechanizmów zasilania, udało się stworzyć w pełni funkcjonalną infrastrukturę bazodanową obsługującą złożone procesy biblioteczne.

Pierwsza część rozdziału koncentrowała się na **Definicji fizycznej bazy danych (Zadanie 1)**, gdzie dokonano implementacji schematów dla dwóch wiodących silników relacyjnych: PostgreSQL i SQLite. Dla środowiska PostgreSQL przygotowano zaawansowane skrypty DDL (Data Definition Language) wykorzystujące natywne typy danych i rygorystyczne więzy integralności, obejmujące tabele takie jak Ksiazki, Wypozyczenia, Autorzy, Kategorie i Czytelnicy. W przypadku SQLite, schemat został zoptymalizowany pod względem jego ograniczeń typowania, zachowując jednocześnie funkcjonalność systemu poprzez jawne deklaracje kluczy obcych.

Druga część rozdziału poświęcona została **Mechanizmowi zasilania bazy danych (Zadanie 2)**. Dane demonstracyjne przygotowano w formacie CSV, który zapewnia elastyczność i łatwość edycji poza systemem bazodanowym. Implementacja mechanizmu importu oparta została na technice batch insert z użyciem biblioteki psycopg w języku Python. Wybór metody ``executemany()`` zapewnia optymalny kompromis między uniwersalnością a wydajnością, pozwalając na szybkie wstawienie wielu rekordów w jednej transakcji z jednoczesnym zabezpieczeniem przedSQL Injection poprzez sparametryzowane zapytania.

Automatyzacja procesu inicjalizacji systemu za pomocą skryptów Python stanowi znaczący wkład w praktyczność rozwiązania, umożliwiając łatwe replikowanie i testowanie bazy danych w różnych środowiskach. Zastosowanie Context Managerów zapewnia bezpieczne zarządzanie transakcjami i zasobami bazy danych.

Niniejszy projekt stanowi kompletne studium cyklu życia relacyjnej bazy danych – od teoretycznego modelowania (Rozdziały 1-3) poprzez praktyczną implementację (Rozdział 4) – demonstrując profesjonalne podejście do administracji, projektowania i eksploatacji systemów bazodanowych.
