================================================
Rozdział 5: Zapytania do bazy danych
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wstęp
=====

Niniejszy rozdział stanowi praktyczną realizację zadania polegającego na stworzeniu funkcji 
Python, które wykonują zaawansowane zapytania SQL do bazy danych bibliotecznego systemu 
zarządzania wypożyczeniami.

Rozdział obejmuje:

1. **Implementację funkcji w Python** – komprehensywny moduł zawierający 10+ funkcji 
   obsługujących PostgreSQL i SQLite
2. **Zaawansowane techniki SQL** – selekcje, agregacje, złączenia, operatory zbiorowe 
   i podzapytania
3. **Automatyczną dokumentację Sphinx** – ciągnięcie docstringów z modułu kodu
4. **Testowanie w JupyterLab** – środowisko do interaktywnego eksperymentowania

Architektura modułu db_queries
===============================

Moduł ``db_queries.py`` zorganizowany jest w logiczne sekcje:

.. code-block:: text

    ├── Połączenia do baz danych (PostgreSQL, SQLite)
    ├── Funkcje selekcji z funkcjami wierszowymi (4 funkcje)
    ├── Funkcje agregujące - GROUP BY, HAVING (2 funkcje)
    ├── Funkcje złączeń - JOINS (2 funkcje)
    ├── Operatory zbiorowe - UNION, NOT IN, EXCEPT (2 funkcje)
    ├── Podzapytania - CTE, Subqueries (2 funkcje)
    └── Funkcje pomocnicze - execute_query()

Każda funkcja istnieje w dwóch wariantach:
- ``*_postgres()`` – optimalizowana dla PostgreSQL
- ``*_sqlite()`` – optimalizowana dla SQLite

Sekcja 5.1: Funkcje selekcji z funkcjami wierszowymi
======================================================

Funkcje tej grupy demonstrują podstawowe operacje selekcji połączone z funkcjami 
wierszowymi takimi jak ``COUNT()``, ``MIN()``, ``MAX()``, ``UPPER()``, ``CONCATENATION``.

Query 1: Autorzy z liczbą napisanych książek
---------------------------------------------

.. autofunction:: modules.db_queries.query_1_autorzy_liczba_ksiazek_postgres
   :noindex:

**Cel zapytania:** Pobierz statystyki autorów - ile książek napisał każdy autor, 
jaka była data jego pierwszej publikacji.

**Koncepty SQL:**
- ``COUNT(DISTINCT k.ID_Ksiazki)`` – funkcja agregująca
- ``MIN(k.Rok_Wydania)`` – minimum wartości w grupie
- ``UPPER()`` – funkcja wierszowa dla transformacji tekstu
- ``LEFT JOIN`` – złączenie z danymi niezobowiązującymi
- ``GROUP BY`` – grupowanie wyników
- ``HAVING`` – filtrowanie po agregacji

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_1_autorzy_liczba_ksiazek_sqlite
   :noindex:


Query 2: Czytelnicy z nieobecnościami i czasem wypożyczenia
-----------------------------------------------------------

.. autofunction:: modules.db_queries.query_2_czytelnicy_aktivni_postgres
   :noindex:

**Cel zapytania:** Zidentyfikuj czytelników, którzy mają wypożyczone książki 
(``Data_Zwrotu IS NULL``) i oblicz, ile dni minęło od wypożyczenia.

**Koncepty SQL:**
- ``CAST(...AS INTEGER)`` – konwersja typów
- ``CURRENT_DATE`` – funkcja zwracająca bieżącą datę
- ``MAX()`` – maksymalna wartość (ostatnia data)
- ``WHERE ... IS NULL`` – filtrowanie wartości pustych
- ``INNER JOIN`` – łączenie ze zmuszającymi warunkami

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_2_czytelnicy_aktivni_sqlite
   :noindex:


Sekcja 5.2: Funkcje agregujące i GROUP BY
===========================================

Funkcje w tej sekcji skupiają się na operacjach agregujących, obliczaniu statystyk 
dla grup danych i stosowaniu zaawansowanych operatorów filtrujących.

Query 3: Statystyki kategorii książek
---------------------------------------

.. autofunction:: modules.db_queries.query_3_kategorie_statystyki_postgres
   :noindex:

**Cel zapytania:** Dla każdej kategorii oblicz statystyki:
- Ile jest książek w kategorii
- Średni rok wydania
- Ile razy książki z tej kategorii były wypożyczane
- Średnia liczba wypożyczeń na jedną książkę (popularność)

**Koncepty SQL:**
- ``COUNT(DISTINCT kb.ID_Ksiazki)`` – liczba unikatowych książek
- ``AVG()`` – średnia arytmetyczna
- ``ROUND(..., 2)`` – zaokrąglanie do 2 miejsc po przecinku
- ``NULLIF()`` – unikanie dzielenia przez zero
- ``HAVING COUNT(*) > 0`` – filtrowanie grup z danymi
- Triple ``LEFT JOIN`` – łączenie 3 tabel

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_3_kategorie_statystyki_sqlite
   :noindex:


Query 4: Top 10 najaktywniejszych czytelników
----------------------------------------------

.. autofunction:: modules.db_queries.query_4_najaktywniejsi_czytelnicy_postgres
   :noindex:

**Cel zapytania:** Rankling czytelników: którzy najczęściej wypożyczają książki 
i ile różnych tytułów czytają?

**Koncepty SQL:**
- ``COUNT()`` – całkowita liczba wypożyczeń
- ``COUNT(DISTINCT w.ID_Ksiazki)`` – liczba unikatowych książek
- ``ORDER BY ... DESC LIMIT 10`` – top N rezultaty
- Agregacja na wielokolumnowych klawiszach

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_4_najaktywniejsi_czytelnicy_sqlite
   :noindex:


Sekcja 5.3: Funkcje złączeń (JOINS)
====================================

Funkcje w tej sekcji demonstrują zaawansowane techniki łączenia tabel oraz filtrowanie 
wyników na podstawie relacji między tabelami.

Query 5: Katalog książek z pełnymi informacjami
------------------------------------------------

.. autofunction:: modules.db_queries.query_5_ksiazki_z_pelnymi_informacjami_postgres
   :noindex:

**Cel zapytania:** Pobierz kompletny katalog wszystkich książek z informacjami 
o autorze, kategorii i aktualnych wypożyczeniach.

**Koncepty SQL:**
- Triple ``LEFT JOIN`` – złączenie 3 tabel z każdą opcjonalnie
- ``COALESCE()`` – zastąpienie NULL wartości domyślnymi tekstami
- ``COUNT(CASE WHEN ... THEN 1 END)`` – warunkowe liczenie
- Grupowanie po wszystkich kolumnach SELECT bez agregacji

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_5_ksiazki_z_pelnymi_informacjami_sqlite
   :noindex:


Query 6: Historia wypożyczeń konkretnego czytelnika
----------------------------------------------------

.. autofunction:: modules.db_queries.query_6_historia_wypozyczen_czytelnika_postgres
   :noindex:

**Cel zapytania:** Dla danego ID czytelnika pobierz kompletną historię jego 
wypożyczeń: jakie książki, od jakich autorów, daty, status zwrotu.

**Koncepty SQL:**
- Parametryzowane zapytanie ``WHERE w.ID_Czytelnika = %s`` (PostgreSQL) 
  lub ``?`` (SQLite) – ochrona przed SQL Injection
- ``CASE WHEN ... ELSE ... END`` – logika warunkowa
- ``INNER JOIN`` – pobieranie tylko pasujących rekordów (tylko czytelnika ze zwrotami)
- ``ORDER BY ... DESC`` – chronologiczny porządek wsteczny

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_6_historia_wypozyczen_czytelnika_sqlite
   :noindex:


Sekcja 5.4: Operatory zbiorowe
==============================

Funkcje demonstrujące operatory UNION, NOT IN, EXCEPT i EXISTS do złożonych 
operacji zbiorowych na zbiorach danych.

Query 7: Porównanie autorów i czytelników
------------------------------------------

.. autofunction:: modules.db_queries.query_7_autorzy_i_czytelnicy_porownanie_postgres
   :noindex:

**Cel zapytania:** Znajdź osoby, które są jednocześnie autorami i czytelnikami 
(mają to samo imię i nazwisko w obu tabelach).

**Koncepty SQL:**
- ``UNION`` – połączenie wyników z dwóch SELECT bez duplikatów
- ``EXISTS`` – egzystencjalny operator subquery
- Porównanie dwóch zbiorów na podstawie kilku kolumn
- ``ORDER BY`` na wyniku połączenia

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_7_autorzy_i_czytelnicy_porownanie_sqlite
   :noindex:


Query 8: Książki bez wypożyczeń
--------------------------------

.. autofunction:: modules.db_queries.query_8_ksiazki_bez_wypozyczen_postgres
   :noindex:

**Cel zapytania:** Zidentyfikuj książki, które nigdy nie były wypożyczane - potencjalni 
kandydaci do usuniętcia lub promocji.

**Koncepty SQL:**
- ``NOT IN (subquery)`` – operator zapamiętujący przeciwny wybór
- ``SELECT DISTINCT ID_Ksiazki FROM Wypozyczenia`` – zbiór książek, które były wypożyczane
- ``LEFT JOIN`` z ``COALESCE()`` – obsługa brakujących wpisów
- Rozumienie różnicy między ``NOT IN`` a ``LEFT JOIN ... IS NULL``

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_8_ksiazki_bez_wypozyczen_sqlite
   :noindex:


Sekcja 5.5: Podzapytania i CTE (Common Table Expressions)
==========================================================

Funkcje demonstrujące zaawansowane techniki podzapytań, Common Table Expressions (WITH), 
oraz okna funkcji.

Query 9: Książki powyżej średniej wypożyczalności
--------------------------------------------------

.. autofunction:: modules.db_queries.query_9_ksiazki_powyzej_sredniej_postgres
   :noindex:

**Cel zapytania:** Oblicz średnią liczbę wypożyczeń na książkę w całej bibliotece, 
następnie wyświetl książki, które są wypożyczane częściej niż średnia.

**Koncepty SQL:**
- ``WITH ... AS`` (CTE) – nazwiązana ekspresja tabelaryczna
- Zagnieżdżone podzapytania
- ``AVG()`` na pośrednim agregowaniu
- ``HAVING COUNT(...) > (SELECT ...)`` – porównanie z rezultatem subquery
- Budowanie skomplikowanej logiki krok po kroku

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_9_ksiazki_powyzej_sredniej_sqlite
   :noindex:


Query 10: Analiza czasowa - trendy wypożyczeń per kwartał
----------------------------------------------------------

.. autofunction:: modules.db_queries.query_10_analiza_czasowa_wypozyczen_postgres
   :noindex:

**Cel zapytania:** Analizuj sezonowość biblioteki: ile było wypożyczeń każdego 
kwartału, czy notujemy wzrost czy spadek liczby wypożyczeń?

**Koncepty SQL:**
- ``EXTRACT(QUARTER FROM ...)`` i ``EXTRACT(YEAR FROM ...)`` – ekstrakcja części daty
- ``LAG(...) OVER (ORDER BY ...)`` – okna funkcji (window functions)
- ``CASE`` z warunkami porównującymi do poprzedniego wiersza
- Analiza trendów: wzrost/spadek/stabilizacja
- Kompleksowa analiza czasowa z zaawansowanym SQL

**Wariant SQLite:**

.. autofunction:: modules.db_queries.query_10_analiza_czasowa_wypozyczen_sqlite
   :noindex:

Sekcja 5.6: Funkcje pomocnicze
===============================

Moduł zawiera również uniwersalne funkcje do wykonywania dowolnych zapytań SQL:

.. autofunction:: modules.db_queries.execute_query_postgres
   :noindex:

.. autofunction:: modules.db_queries.execute_query_sqlite
   :noindex:

Przewodnik po złożoności zapytań SQL
=====================================

Tabela poniższa podsumowuje koncepty SQL używane w każdym zapytaniu:

.. list-table::
   :header-rows: 1
   :widths: 10, 15, 15, 15, 15, 15

   * - Query
     - Selekcja
     - Agregacja
     - Złączenia
     - Operatory
     - Zaawansowane
   * - Query 1
     - ✓
     - COUNT, MIN, UPPER
     - LEFT JOIN
     - GROUP BY, HAVING
     - Funkcje wierszowe
   * - Query 2
     - ✓
     - COUNT, MAX
     - INNER JOIN
     - WHERE IS NULL
     - Obliczenia dat
   * - Query 3
     - ✓
     - COUNT, AVG, ROUND
     - 3× LEFT JOIN
     - GROUP BY, HAVING
     - NULLIF, Triple JOIN
   * - Query 4
     - ✓
     - COUNT (×2)
     - INNER JOIN
     - GROUP BY
     - LIMIT, Ranking
   * - Query 5
     - ✓
     - COUNT (warunkowy)
     - 3× LEFT JOIN
     - COALESCE
     - CASE WHEN
   * - Query 6
     - ✓
     - -
     - 2× INNER JOIN
     - WHERE z parametrem
     - Parametryzacja
   * - Query 7
     - ✓
     - -
     - EXISTS
     - UNION
     - Operatory zbiorowe
   * - Query 8
     - ✓
     - COUNT (DISTINCT)
     - LEFT JOIN
     - NOT IN
     - Podzapytanie
   * - Query 9
     - ✓
     - COUNT, AVG
     - LEFT JOIN
     - WITH, HAVING
     - CTE, Podzapytanie
   * - Query 10
     - ✓
     - COUNT
     - -
     - EXTRACT
     - LAG, Okna funkcji

Testowanie w JupyterLab
=======================

Poniższy kod demonstruje, jak wykorzystać moduł w JupyterLab:

.. code-block:: python

    # Importowanie modułu
    import sys
    sys.path.insert(0, '/path/to/modules')
    from db_queries import *
    
    # Konfiguracja PostgreSQL
    pg_config = {
        'host': 'localhost',
        'dbname': 'biblioteka',
        'user': 'postgres',
        'password': 'haslo'
    }
    
    # Konfiguracja SQLite
    sqlite_path = '/path/to/biblioteka.db'
    
    # Testowanie Query 1 - PostgreSQL
    authors = query_1_autorzy_liczba_ksiazek_postgres(pg_config)
    for author in authors:
        print(f"{author['autor']}: {author['liczba_ksiazek']} książek")
    
    # Testowanie Query 3 - SQLite
    categories = query_3_kategorie_statystyki_sqlite(sqlite_path)
    for cat in categories:
        print(f"{cat['kategoria']}: {cat['liczba_ksiazek']} książek, "
              f"śr. {cat['srednia_wypozyczen_per_ksiazke']} wyp/książka")
    
    # Testowanie Query 6 z parametrem
    reader_id = 1
    history = query_6_historia_wypozyczen_czytelnika_postgres(pg_config, reader_id)
    for book in history:
        print(f"{book['tytul']} - {book['status']}")

Zarządzanie połączeniami i bezpieczeństwo
==========================================

Wszystkie funkcje w module:

1. **Zarządzają automatycznie połączeniami** – używają context managerów (``with``)
2. **Parametryzują zapytania** – ochrona przed SQL Injection:
   
   .. code-block:: python
   
       # ✓ BEZPIECZNIE (parametryzacja)
       cursor.execute("SELECT * FROM Ksiazki WHERE ID = %s", (book_id,))
       
       # ✗ NIEBEZPIECZNIE (string formatting)
       cursor.execute(f"SELECT * FROM Ksiazki WHERE ID = {book_id}")

3. **Zwracają słowniki Python** – łatwe do przetwarzania i konwersji do JSON
4. **Obsługują wyjątki** – każda funkcja ma ``try-except``

Wdrażanie na serwerze programuję.eu
====================================

Moduł ``db_queries.py`` został umieszczony w repozytorium w katalogu:

.. code-block:: text

    /baguetedev/Bazy-Danych-1/modules/db_queries.py

Ścieżka dostępu na serwerze programuję.eu:

.. code-block:: text

    /var/www/projekty/baguetedev/Bazy-Danych-1/modules/db_queries.py

Do używania w JupyterLab:

.. code-block:: python

    import sys
    sys.path.insert(0, '/var/www/projekty/baguetedev/Bazy-Danych-1')
    from modules.db_queries import *

Podsumowanie
============

Rozdział 5 realizuje komprehensywne zadanie zapytań do bazy danych:

1. **10 zaawansowanych funkcji SQL** – każda demonstruje inny aspekt języka zapytań
2. **Podwójne wsparcie** – PostgreSQL i SQLite w każdej funkcji
3. **Dokumentacja Sphinx** – automatycznie ścieżki z kodu
4. **Bezpieczeństwo** – parametryzacja, zarządzanie wyjątkami, context managery
5. **Praktyczne zastosowania** – wszystkie zapytania mają realny sens w systemie bibliotecznym

Funkcje pokrywają:
- ✓ Selekcję danych i funkcje wierszowe
- ✓ Funkcje agregujące (COUNT, AVG, MIN, MAX)
- ✓ Połączenia wielotabelowe (LEFT JOIN, INNER JOIN, tripple JOIN)
- ✓ Operatory zbiorowe (UNION, NOT IN, EXISTS)
- ✓ Podzapytania (CTE, subqueries)
- ✓ Okna funkcji i analizę czasową (LAG, EXTRACT)

Zasobami zewnętrznymi są:

- Moduł Python: `modules/db_queries.py <https://github.com/baguetedev/Bazy-Danych-1/blob/main/modules/db_queries.py>`_
- JupyterLab na programuję.eu: ``/var/www/projekty/baguetedev/...``
