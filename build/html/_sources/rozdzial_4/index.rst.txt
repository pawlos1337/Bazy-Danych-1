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
Niniejszy rozdział wieńczy etap projektowania i wdrażania struktury relacyjnej bazy danych dla systemu zarządzania biblioteką. Poprzez transformację modelu logicznego do postaci fizycznej, [...]

Dodatkowo, proces inicjalizacji systemu został zautomatyzowany dzięki przygotowaniu skryptu w języku Python. Wykorzystanie plików CSV oraz mechanizmu wsadowego wstawiania danych (batch insert[...]
