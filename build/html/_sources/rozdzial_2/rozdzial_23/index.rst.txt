================================================
Kontrola i konserwacja
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wprowadzenie
============
Współczesne systemy relacyjnych baz danych to wysoce skomplikowane środowiska, które wymagają ciągłego i proaktywnego nadzoru, aby zagwarantować wysoką dostępność, niezawodność oraz wydajność. Administracja takimi systemami stanowi złożone zagadnienie wymagające zarówno wiedzy teoretycznej, jak i praktycznego doświadczenia w zarządzaniu infrastrukturą informatyczną.

Zarządzanie przestrzenią i mechanizm współbieżności
===================================================
PostgreSQL opiera swoje działanie na zaawansowanej architekturze określanej jako Multi-Version Concurrency Control (MVCC). Technologia ta pozwala na równoległy odczyt i zapis danych bez wzajemnego blokowania się transakcji, co stanowi fundamentalną zaletę w środowiskach wieloużytkownikowych o wysokim natężeniu operacji.

Aby zapobiec zjawisku drastycznego puchnięcia tabel oraz degradacji wydajności operacji wejścia i wyjścia, konieczna jest regularna konserwacja na poziomie nośnika danych:

* **VACUUM:** Podstawowy proces konserwacyjny odzyskujący miejsce po martwych krotkach. Oznacza on wolne obszary jako dostępne do ponownego zapisu przez nowe instrukcje, zapobiegając niekontrolowanemu wzrostowi rozmiarów tabel na dysku.
* **VACUUM FULL:** Znacznie bardziej inwazyjna wersja operacji, która fizycznie przebudowuje strukturę całej tabeli i trwale zwraca wolne miejsce do systemu operacyjnego. Operacja ta wymaga jednak zablokowania całej tabeli i powinna być wykonywana w godzinach niskiego obciążenia.
* **AUTOVACUUM:** W nowoczesnych środowiskach produkcyjnych utrzymanie czystości dyskowej powierza się wbudowanemu procesowi pracującemu w tle. Monitoruje on na bieżąco statystyki zmian i automatycznie wyzwala operacje czyszczenia, eliminując potrzebę ręcznej interwencji administratora.

Zaniedbanie procesu czyszczenia w systemach o wysokiej rotacji danych może doprowadzić nie tylko do spadku wydajności, ale w skrajnych przypadkach do wyczerpania identyfikatorów transakcji, co prowadzi do całkowitego zamrożenia bazy.

.. code-block:: sql

    -- Przykładowe wymuszenie manualnej konserwacji z analizą statystyk dla tabeli
    VACUUM (VERBOSE, ANALYZE) Wypozyczenia;

Optymalizacja i statystyki planisty zapytań
===========================================
Kolejnym filarem utrzymania sprawności systemu jest kontrola nad optymalizatorem, zwanym planistą zapytań. Silnik bazy danych przed wykonaniem jakiejkolwiek skomplikowanej kwerendy analizuje dostępne drogi realizacji i wybiera najefektywniejszą z punktu widzenia kosztów obliczeniowych.

Aby planista mógł podejmować optymalne decyzje, musi opierać się na wysoce dokładnych i aktualnych statystykach dotyczących rozkładu danych. Obejmują one między innymi histogramy wartości w kolumnach, liczby odrębnych wartości (distinct count), oraz rozmiary tabel i indeksów.

* Instrukcja **ANALYZE** służy do natychmiastowego odświeżenia tych metadanych. Baza pobiera losową próbkę wierszy i na jej podstawie aktualizuje wewnętrzne tabele systemowe, co pozwala uniknąć błędnych oszacowań planu wykonania.
* Bieżące profilowanie wydajności realizowane jest natomiast przy pomocy instrukcji **EXPLAIN ANALYZE**. Narzędzie to uruchamia zapytanie, po czym zwraca nie tylko wynik, ale również szczegółowy opis planu wykonania wraz z rzeczywistymi czasy i liczbami wierszy na każdym kroku.

.. code-block:: sql

    -- Kontrola planu wykonania zapytania z rzeczywistym pomiarem czasu
    EXPLAIN ANALYZE
    SELECT c.Imie, c.Nazwisko, k.Tytul
    FROM Czytelnicy c
    JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika
    JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki
    WHERE w.Data_Zwrotu IS NULL;

Bezpieczeństwo i rygorystyczna kontrola dostępu
===============================================
Bezpieczeństwo danych stanowi absolutny priorytet każdej administracji systemami informatycznymi. Nowoczesne podejście do ochrony baz danych całkowicie odchodzi od wykorzystywania globalnych kont administratora na rzecz zaawansowanego systemu uprawnień opartego na rolach (RBAC – Role-Based Access Control).

System zabezpieczeń środowiska PostgreSQL pozwala na niezwykle elastyczną gradację uprawnień. Definiuje się dedykowane role systemowe przypisane do konkretnych mikrousług lub modułów aplikacji, z precyzyjnie określonymi prawami dostępu do pojedynczych schematów, tabel, a nawet kolumn.

Kluczowym konceptem jest wdrożenie zasady najmniejszych uprawnień (Principle of Least Privilege). Rola wykorzystywana przez aplikację powinna dysponować prawami pozwalającymi wyłącznie na modyfikację danych niezbędnych do jej funkcjonowania, bez dostępu do danych wrażliwych czy możliwości zmiany struktury bazy.

.. code-block:: sql

    -- Przykład implementacji bezpiecznej polityki kontroli dostępu
    CREATE ROLE app_user WITH LOGIN PASSWORD 'TrudneHaslo123';
    GRANT CONNECT ON DATABASE biblioteka_db TO app_user;
    GRANT USAGE ON SCHEMA public TO app_user;
    GRANT SELECT, INSERT ON Wypozyczenia TO app_user;

Strategie zabezpieczania przed utratą danych
============================================
Nawet najlepiej zoptymalizowany i zabezpieczony system informatyczny jest narażony na błędy ludzkie lub awarie infrastruktury sprzętowej. Dlatego odpowiednia polityka wykonywania kopii zapasowych stanowi ostateczną linię obrony i jest absolutnie niezbędna dla każdej produkcyjnej instancji bazy danych.

Kopie logiczne polegają na ekstrakcji danych z bazy do postaci czystego skryptu języka SQL lub dedykowanego formatu archiwalnego. Narzędzia realizujące to zadanie gwarantują przenośność danych między platformami i wersjami silnika, jednak proces przywracania jest czasochłonny i może nie przywrócić wszystkich zmian z ostatnich minut przed awarią.

Dlatego w krytycznych środowiskach produkcyjnych stosuje się kopie fizyczne połączone z archiwizacją dzienników wyprzedzających. Dzienniki te rejestrują absolutnie każdą zmianę bajtu na poziomie magazynu, co umożliwia odtworzenie bazy do dowolnego punktu w przeszłości z dokładnością do sekundy.

Podsumowanie
============
Prawidłowa kontrola i konserwacja środowiska bazodanowego to wielowymiarowy proces, który nie ma punktu końcowego, lecz trwa przez cały cykl życia oprogramowania. Złożoność nowoczesnych systemów relacyjnych wymaga holistycznego podejścia łączącego automatyzację, monitoring i ciągłe doskonalenie.

Samo zaprojektowanie zgodnego ze sztuką schematu relacyjnego jest zaledwie początkiem pracy. Stabilność aplikacji zależy w równej mierze od rygorystycznego zarządzania fizyczną strukturą danych, optymalizacji wykonywanych operacji oraz wdrażania wielowarstwowych strategii bezpieczeństwa i ochrony przed awarią.

Holistyczne spojrzenie na administrację PostgreSQL, obejmujące zarówno automatyzację procesów porządkujących pamięć, jak i ciągłe monitorowanie planów wykonania zapytań, pozwala na budowanie systemów, które są nie tylko funkcjonalne, ale także odpornie i niezawodne w najbardziej wymagających warunkach produkcyjnych.
