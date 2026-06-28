==========================================================
Implementacja fizyczna i zasilanie bazy danych
==========================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Definicja fizyczna bazy danych (Zadanie 1)
==========================================
Na podstawie opracowanych wcześniej modeli logicznych przygotowano skrypty DDL (Data Definition Language) dla dwóch docelowych silników relacyjnych baz danych: PostgreSQL oraz SQLite. Kody te przygotowały solidną fundamentę dla skutecznego przechowywania i zarządzania danymi biblioteki.

Pełny kod źródłowy definicji bazy danych (skrypty DDL) oraz mechanizmy zasilające znajdują się w dedykowanym repozytorium projektu: 
`GitHub - Bazy-Danych-pliki <https://github.com/pawlos1337/Bazy-danych-pliki>`_

Skrypt dla środowiska PostgreSQL
--------------------------------
Środowisko PostgreSQL pozwala na wykorzystanie zaawansowanych, natywnych typów danych oraz rygorystyczne egzekwowanie więzów integralności. W poniższym skrypcie kluczowym elementem jest użycie więzów klucza obcego (FOREIGN KEY) w celu zapewnienia spójności referencyalnej między tabelami.

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
W silniku SQLite struktura ulega pewnemu uproszczeniu z powodu mniejszej rygorystyczności typowania oraz bardzo ograniczonej liczby wbudowanych klas typów danych (np. brak odrębnego typu daty). Pomimo ograniczeń, SQLite pozostaje niezawodnym rozwiązaniem do prototypowania i mniejszych aplikacji.

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
Dane do importu przygotowano w niezależnym formacie płaskim CSV (Comma-Separated Values). Takie podejście pozwala na łatwą edycję danych poza systemem bazodanowym. Poniżej zaprezentowano wybrane kategorie książek przygotowane w formacie CSV.

.. code-block:: text

    Nazwa_Kategorii
    Fantastyka
    Kryminał
    Literatura faktu
    Poezja
    Horror

Implementacja mechanizmu importu
--------------------------------
Do zaimportowania powyższych danych wybrano mechanizm wprowadzania wielowartościowego oparty na technice **INSERT (multi-value/batch)**. Rozwiązanie zrealizowano z wykorzystaniem języka Python wraz z biblioteką psycopg do komunikacji z bazą PostgreSQL oraz wbudowaną biblioteką sqlite3 dla bazy SQLite.

Wybór tego mechanizmu podyktowany jest kompromisem między uniwersalnością a wydajnością. Użycie metody ``executemany()`` na obiekcie kursora bazy danych pozwala na szybkie wstawienie wielu rekordów bez konieczności wykonywania zapytania dla każdego wiersza osobno.

Poniżej przedstawiono fragment skryptu aplikacyjnego odpowiedzialnego za odczyt z pliku i zasilenie tabel dla PostgreSQL:

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

    if __name__ == "__main__":
        # Dane logowania do bazy (do uzupełnienia rzeczywistymi danymi z laboratorium)
        konfiguracja_bazy = {
            "dbname": "student15db4",
            "user": "student15",
            "password": "fwbmfhgxqdZNP",
            "host": "localhost", 
            "port": "5432"
        }
        # Uruchomienie procesu
        dane_z_pliku = wczytaj_dane_csv('kategorie.csv')
        if dane_z_pliku:
            importuj_do_postgres(dane_z_pliku, konfiguracja_bazy)

Analogiczny skrypt przygotowano do obsługi plikowej bazy danych SQLite, korzystając z tej samej metodyki odczytu wsadowego:

.. code-block:: python

    import sqlite3
    import csv
    import os

    # Funkcja wsadowego importu do SQLite
    def importuj_do_sqlite(kategorie_do_importu, sciezka_bazy):
        try:
            # Nawiązanie połączenia z plikiem bazy danych (.db)
            with sqlite3.connect(sciezka_bazy) as conn:
                cursor = conn.cursor()
                
                # Sparametryzowane zapytanie (? dla SQLite)
                zapytanie_sql = "INSERT INTO Kategorie (Nazwa_Kategorii) VALUES (?)"
                
                # Wykonanie wsadowe
                cursor.executemany(zapytanie_sql, kategorie_do_importu)
                
                # Konieczne zatwierdzenie transakcji
                conn.commit()
                
                print(f"Pomyślnie zaimportowano {len(kategorie_do_importu)} rekordów do SQLite.")
        except sqlite3.Error as e:
            print(f"Wystąpił błąd bazy SQLite: {e}")

    if __name__ == "__main__":
        plik_bazy = 'biblioteka.db'
        plik_csv = 'kategorie.csv'
        
        # Sprawdzenie czy plik CSV istnieje przed importem
        if os.path.exists(plik_csv):
            dane_z_pliku = wczytaj_dane_csv(plik_csv)
            importuj_do_sqlite(dane_z_pliku, plik_bazy)
        else:
            print(f"Brak pliku {plik_csv}. Upewnij się, że znajduje się w tym samym folderze.")

Podsumowanie
============

Niniejszy rozdział wieńczy etap projektowania i wdrażania struktury relacyjnej bazy danych dla systemu zarządzania biblioteką. Poprzez transformację modelu logicznego do postaci fizycznej osiągnięto kompletne i funkcjonalne rozwiązanie.

Pierwsza część rozdziału koncentrowała się na **Definicji fizycznej bazy danych (Zadanie 1)**, gdzie dokonano implementacji schematów dla dwóch wiodących silników relacyjnych: PostgreSQL i SQLite, stanowiących praktyczną alternatywę w zależności od wymagań skalowalności oraz zasobów dostępnych w środowisku produkcyjnym.

Druga część rozdziału poświęcona została **Mechanizmowi zasilania bazy danych (Zadanie 2)**. Dane demonstracyjne przygotowano w formacie CSV, który zapewnia elastyczność i łatwość edycji zarówno dla administratorów baz danych, jak i dla użytkowników końcowych systemu.

Automatyzacja procesu inicjalizacji systemu za pomocą skryptów Python stanowi znaczący wkład w praktyczność rozwiązania, umożliwiając łatwe replikowanie i testowanie bazy danych w różnych środowiskach bez konieczności wykonywania repetycyjnych czynności manualnych.

Niniejszy projekt stanowi kompletne studium cyklu życia relacyjnej bazy danych – od teoretycznego modelowania (Rozdziały 1-3) poprzez praktyczną implementację (Rozdział 4) – demonstrując całkowity proces od koncepcji do produkcyjnego systemu zarządzania danymi.
