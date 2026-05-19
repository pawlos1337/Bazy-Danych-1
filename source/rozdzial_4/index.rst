===========================================================
Rozdział 4: Implementacja fizyczna i zasilanie bazy danych
===========================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski



1. Definicja fizyczna bazy danych (Zadanie 1)
=============================================
Na podstawie opracowanych wcześniej modeli logicznych przygotowano skrypty DDL (Data Definition Language) dla dwóch docelowych silników relacyjnych baz danych: PostgreSQL oraz SQLite. Kody te posłużyły do utworzenia struktur w bazach dostępnych na serwerze laboratoryjnym oraz przez sieć Internet.

1.1. Skrypt dla środowiska PostgreSQL
-------------------------------------
Środowisko PostgreSQL pozwala na wykorzystanie zaawansowanych, natywnych typów danych oraz rygorystyczne egzekwowanie więzów integralności. W poniższym skrypcie kluczowym elementem jest użycie pseudo-typu ``SERIAL`` dla automatycznej generacji kluczy głównych oraz typów o stałej lub ograniczonej długości (``VARCHAR``, ``SMALLINT``, ``DATE``) dla optymalizacji przechowywania danych. Relacje między tabelami zapewniane są przez twarde klauzule ``REFERENCES``.

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

1.2. Skrypt dla środowiska SQLite
---------------------------------
W silniku SQLite struktura ulega pewnemu uproszczeniu z powodu mniejszej rygorystyczności typowania oraz bardzo ograniczonej liczby wbudowanych klas typów danych (np. brak odrębnego typu daty). Z tego względu zastosowano typ ``TEXT`` dla dat i łańcuchów znaków. Ponadto w SQLite relacje kluczy obcych deklaruje się w osobnej klauzuli ``FOREIGN KEY`` na końcu definicji tabeli, a automatyczna inkrementacja klucza realizowana jest atrybutem ``AUTOINCREMENT``.

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

2. Mechanizm zasilania bazy danych (Zadanie 2)
==============================================
Posiadając gotową strukturę bazy, należało wyposażyć ją w dane demonstracyjne. Przygotowano zbiór danych testowych, które zostały poddane wsadowemu ładowaniu (batch import).

2.1. Formatyzacja danych (Pliki CSV)
------------------------------------
Dane do importu przygotowano w niezależnym formacie płaskim CSV (Comma-Separated Values). Takie podejście pozwala na łatwą edycję danych poza systemem bazodanowym. Poniżej zaprezentowano wycinek pliku ``dane_kategorie.csv``:

.. code-block:: text

    Nazwa_Kategorii
    Fantastyka
    Kryminał
    Literatura faktu
    Poezja
    Horror

2.2. Implementacja mechanizmu importu 
-------------------------------------
Do zaimportowania powyższych danych wybrano mechanizm wprowadzania wielowartościowego oparty na technice **INSERT (multi-value/batch)**. Rozwiązanie zrealizowano z wykorzystaniem języka Python oraz dedykowanego sterownika ``psycopg``.

Wybór tego mechanizmu podyktowany jest kompromisem między uniwersalnością a wydajnością. Użycie metody ``executemany()`` na obiekcie kursora bazy danych pozwala na szybkie wstawienie wielu rekordów w ramach pojedynczej transakcji sieciowej. Jest to rozwiązanie znacznie bardziej optymalne czasowo i obciążeniowo niż wykonywanie pojedynczych instrukcji ``INSERT`` iteracyjnie w pętli. Opcjonalna klauzula ``COPY`` byłaby szybsza, jednak rozwiązanie oparte o wsadowy ``INSERT`` jest bardziej uniwersalne w architekturze klient-serwer.

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

3. Podsumowanie
===============
Niniejszy rozdział wieńczy etap projektowania i wdrażania struktury relacyjnej bazy danych dla systemu zarządzania biblioteką. Poprzez transformację modelu logicznego do postaci fizycznej, udało się z powodzeniem zaimplementować docelowe schematy w dwóch niezależnych środowiskach bazodanowych: produkcyjnym (PostgreSQL) oraz lokalnym/testowym (SQLite). Opracowane skrypty DDL poprawnie uwzględniają specyfikę obu silników, zachowując przy tym pożądaną architekturę relacyjną.

Dodatkowo, proces inicjalizacji systemu został zautomatyzowany dzięki przygotowaniu skryptu w języku Python. Wykorzystanie plików CSV oraz mechanizmu wsadowego wstawiania danych (batch insert) udowodniło, że możliwe jest szybkie i skalowalne zasilenie bazy niezbędnymi danymi demonstracyjnymi. Wdrożone rozwiązania stanowią solidny, zoptymalizowany fundament do dalszych prac nad logiką biznesową i warstwą aplikacyjną całego projektu.
