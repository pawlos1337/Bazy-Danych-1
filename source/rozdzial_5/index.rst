================================================
Rozdział 5: Zapytania do bazy danych
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wstęp
=====
Niniejszy rozdział stanowi praktyczną realizację zadania polegającego na przygotowaniu zestawu zaawansowanych zapytań SQL do utworzonej bazy danych systemu bibliotecznego. Zapytania te zostały zaimplementowane i hermetyzowane w postaci dedykowanego modułu w języku Python.

W ramach przeprowadzonych prac laboratoryjnych:

1. **Opracowaliśmy kompleksowy moduł** – skrypt zawiera 10 unikalnych funkcji odpytujących bazę, z podziałem na 5 zapytań zoptymalizowanych dla środowiska PostgreSQL oraz 5 dla silnika SQLite.
2. **Zastosowaliśmy zaawansowaną logikę SQL** – odchodząc od prostych selekcji, zaimplementowaliśmy zapytania wykorzystujące wielokrotne złączenia, agregacje, podzapytania skorelowane, operatory zbiorowe oraz okna funkcji (Window Functions).
3. **Przeprowadziliśmy weryfikację w środowisku JupyterLab** – każde zapytanie zostało interaktywnie przetestowane pod kątem wydajności i poprawności zwracanych rezultatów.
4. **Zadbaliśmy o bezpieczeństwo i stabilność** – zapytania korzystające z danych wejściowych zostały w pełni sparametryzowane (ochrona przed SQL Injection), a połączenia z bazą opleciono menedżerami kontekstu.

Przegląd zaimplementowanej logiki biznesowej
===========================================
Struktura zapytań została zaprojektowana w taki sposób, aby odpowiadała na realne problemy analityczne i operacyjne, z którymi mierzy się administracja biblioteki. 

Wykorzystane koncepcje i scenariusze biznesowe:

* **Raportowanie statystyczne i formatowanie (PostgreSQL):** Pobieranie statystyk autorów (liczba książek, rok debiutu) z jednoczesnym formatowaniem tekstu na poziomie bazy danych (``UPPER``) oraz filtrowaniem zagregowanych wyników (``HAVING``).
* **Zarządzanie katalogiem (PostgreSQL):** Generowanie pełnych metadanych o księgozbiorze. Aby uniknąć utraty danych w przypadku książek bez przypisanej kategorii, wykorzystaliśmy potrójne złączenie lewostronne (``LEFT JOIN``) oraz funkcję ``COALESCE``.
* **Analiza historyczna i trendy (PostgreSQL):** Zbadanie dynamiki wypożyczeń na przestrzeni lat z wykorzystaniem Common Table Expressions (``WITH``) oraz zaawansowanych funkcji okna (``LAG() OVER()``) badających różnice między rekordami.
* **Badanie retencji i zaangażowania (SQLite):** Wyliczanie rzeczywistego czasu przetrzymywania woluminów przez czytelników, wykorzystując specyficzne dla SQLite funkcje wierszowe operujące na datach (``julianday``) oraz tworzenie rankingów aktywności (``LIMIT``).
* **Audyt bazy i relacji (PostgreSQL i SQLite):** Detekcja książek "martwych" (nigdy niewypożyczonych) przy pomocy operatora ``NOT IN``, zestawianie książek wydanych powyżej średniej wieku inwentarza (podzapytania skalarne) oraz wykrywanie osób pełniących podwójne role w systemie (operatory ``UNION`` oraz ``EXISTS``).

Przewodnik po złożoności zapytań SQL
====================================
Poniższa tabela szczegółowo mapuje zrealizowane w kodzie zapytania do konkretnych koncepcji z zakresu relacyjnych baz danych omawianych na wykładach:

.. list-table::
   :header-rows: 1
   :widths: 10, 15, 15, 15, 15, 15

   * - Funkcja (Moduł)
     - Selekcja
     - Agregacja
     - Złączenia
     - Operatory
     - Zaawansowane
   * - Query 1 (PG)
     - ✓
     - COUNT, MIN
     - LEFT JOIN
     - GROUP BY, HAVING
     - Wierszowe (UPPER)
   * - Query 2 (PG)
     - ✓
     - COUNT
     - 3× LEFT JOIN
     - GROUP BY
     - Wierszowe (COALESCE)
   * - Query 3 (PG)
     - ✓
     - -
     - -
     - UNION
     - Konsolidacja zbiorów
   * - Query 4 (PG)
     - ✓
     - COUNT
     - -
     - GROUP BY
     - CTE, LAG OVER, EXTRACT
   * - Query 5 (PG)
     - ✓
     - -
     - INNER JOIN
     - WHERE = %s
     - CASE WHEN, Parametryzacja
   * - Query 6 (SQ)
     - ✓
     - -
     - 2× INNER JOIN
     - WHERE IS NOT NULL
     - Wierszowe (julianday, CAST)
   * - Query 7 (SQ)
     - ✓
     - COUNT
     - JOIN
     - GROUP BY
     - LIMIT (Top 10)
   * - Query 8 (SQ)
     - ✓
     - -
     - -
     - NOT IN
     - Podzapytanie filtracyjne
   * - Query 9 (SQ)
     - ✓
     - AVG (w subquery)
     - -
     - WHERE >
     - Podzapytanie skalarne
   * - Query 10 (SQ)
     - ✓
     - -
     - -
     - EXISTS
     - Podzapytanie skorelowane

Środowisko testowe i wdrożenie
==============================
Proces tworzenia, testowania i ostatecznej weryfikacji funkcji odbywał się na przygotowanym infrastrukturze serwerowej przy użyciu notatników.

**Lokalizacja środowiska roboczego:**
Katalog roboczy wraz ze skryptami znajduje się na serwerze programuję.eu:

.. code-block:: text

    /var/www/projekty/baguetedev/Bazy-Danych-1/modules/db_queries.py

**Przykładowy scenariusz wywołania w JupyterLab:**
Poniższy fragment kodu obrazuje sposób, w jaki moduł jest implementowany w docelowym środowisku do pobrania historii konkretnego czytelnika:

.. code-block:: python

    import sys
    sys.path.insert(0, '/var/www/projekty/baguetedev/Bazy-Danych-1')
    from modules.db_queries import *
    
    # Konfiguracja środowiska docelowego
    pg_config = {
        'host': 'localhost',
        'dbname': 'biblioteka',
        'user': 'postgres',
        'password': 'haslo'
    }
    
    # Pobranie sparametryzowanej historii wypożyczeń
    id_czytelnika = 1
    historia = query_5_historia_wypozyczen_czytelnika_postgres(pg_config, id_czytelnika)
    for rekord in historia:
        print(f"Książka: {rekord['tytul']} | Status: {rekord['status_wypozyczenia']}")

Kod źródłowy całego modułu (zawierający pełną obsługę błędów i warianty dla obu baz) został dołączony do naszego publicznego repozytorium projektu: `baguetedev/Bazy-Danych-1 <https://github.com/baguetedev/Bazy-Danych-1/blob/main/modules/db_queries.py>`_.

Dokumentacja interfejsu programistycznego (API)
===============================================
W celu automatyzacji procesu dokumentowania kodu, wykorzystaliśmy mechanizmy udostępniane przez bibliotekę Sphinx. Zamiast manualnie przepisywać informacje o argumentach i zwracanych wartościach, poniższa dokumentacja techniczna została wyekstrahowana bezpośrednio z sformatowanych komentarzy (docstringów) znajdujących się w pliku ``db_queries.py``. Gwarantuje to absolutną spójność logiki w kodzie z niniejszym sprawozdaniem.

.. automodule:: modules.db_queries
   :members:
   :undoc-members:
   :show-inheritance:
