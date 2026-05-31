================================================
Rozdział 1: Kontrola i konserwacja
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wprowadzenie
============
Współczesne systemy relacyjnych baz danych to wysoce skomplikowane środowiska, które wymagają ciągłego i proaktywnego nadzoru, aby zagwarantować wysoką dostępność, niezawodność oraz [...]

Zarządzanie przestrzenią i mechanizm współbieżności
===================================================
PostgreSQL opiera swoje działanie na zaawansowanej architekturze określanej jako Multi-Version Concurrency Control. Technologia ta pozwala na równoległy odczyt i zapis danych bez wzajemnego bl[...]

Aby zapobiec zjawisku drastycznego puchnięcia tabel oraz degradacji wydajności operacji wejścia i wyjścia, konieczna jest regularna konserwacja na poziomie nośnika danych:

* **VACUUM:** Podstawowy proces konserwacyjny odzyskujący miejsce po martwych krotkach. Oznacza on wolne obszary jako dostępne do ponownego zapisu przez nowe instrukcje, zapobiegając niekontrol[...]
* **VACUUM FULL:** Znacznie bardziej inwazyjna wersja operacji, która fizycznie przebudowuje strukturę całej tabeli i trwale zwraca wolne miejsce do systemu operacyjnego. Operacja ta wymaga jed[...]
* **AUTOVACUUM:** W nowoczesnych środowiskach produkcyjnych utrzymanie czystości dyskowej powierza się wbudowanemu procesowi pracującemu w tle. Monitoruje on na bieżąco statystyki zmian i au[...]

Zaniedbanie procesu czyszczenia w systemach o wysokiej rotacji danych może doprowadzić nie tylko do spadku wydajności, ale w skrajnych przypadkach do wyczerpania identyfikatorów transakcji, co[...]

.. code-block:: sql

    -- Przykładowe wymuszenie manualnej konserwacji z analizą statystyk dla tabeli
    VACUUM (VERBOSE, ANALYZE) Wypozyczenia;

Optymalizacja i statystyki planisty zapytań
===========================================
Kolejnym filarem utrzymania sprawności systemu jest kontrola nad optymalizatorem, zwanym planistą zapytań. Silnik bazy danych przed wykonaniem jakiejkolwiek skomplikowanej kwerendy analizuje dz[...]

Aby planista mógł podejmować optymalne decyzje, musi opierać się na wysoce dokładnych i aktualnych statystykach dotyczących rozkładu danych. Obejmują one między innymi histogramy wartoś[...]

* Instrukcja **ANALYZE** służy do natychmiastowego odświeżenia tych metadanych. Baza pobiera losową próbkę wierszy i na jej podstawie aktualizuje wewnętrzne tabele systemowe, co pozwala un[...]
* Bieżące profilowanie wydajności realizowane jest natomiast przy pomocy instrukcji **EXPLAIN ANALYZE**. Narzędzie to uruchamia zapytanie, po czym zwraca nie tylko wynik, ale również szczeg[...]

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
Bezpieczeństwo danych stanowi absolutny priorytet każdej administracji systemami informatycznymi. Nowoczesne podejście do ochrony baz danych całkowicie odchodzi od wykorzystywania globalnych k[...]

System zabezpieczeń środowiska PostgreSQL pozwala na niezwykle elastyczną gradację uprawnień. Definiuje się dedykowane role systemowe przypisane do konkretnych mikrousług lub modułów apli[...]

Kluczowym konceptem jest wdrożenie zasady najmniejszych uprawnień. Rola wykorzystywana przez aplikację powinna dysponować prawami pozwalającymi wyłącznie na modyfikację danych niezbędnych[...]

.. code-block:: sql

    -- Przykład implementacji bezpiecznej polityki kontroli dostępu
    CREATE ROLE app_user WITH LOGIN PASSWORD 'TrudneHaslo123';
    GRANT CONNECT ON DATABASE biblioteka_db TO app_user;
    GRANT USAGE ON SCHEMA public TO app_user;
    GRANT SELECT, INSERT ON Wypozyczenia TO app_user;

Strategie zabezpieczania przed utratą danych
============================================
Nawet najlepiej zoptymalizowany i zabezpieczony system informatyczny jest narażony na błędy ludzkie lub awarie infrastruktury sprzętowej. Dlatego odpowiednia polityka wykonywania kopii zapasow[...]

Kopie logiczne polegają na ekstrakcji danych z bazy do postaci czystego skryptu języka SQL lub dedykowanego formatu archiwalnego. Narzędzia realizujące to zadanie gwarantują przenośność da[...]

Dlatego w krytycznych środowiskach produkcyjnych stosuje się kopie fizyczne połączone z archiwizacją dzienników wyprzedzających. Dzienniki te rejestrują absolutnie każdą zmianę bajtu na[...]

Podsumowanie
============
Prawidłowa kontrola i konserwacja środowiska bazodanowego to wielowymiarowy proces, który nie ma punktu końcowego, lecz trwa przez cały cykl życia oprogramowania. Złożoność nowoczesnych [...]

Samo zaprojektowanie zgodnego ze sztuką schematu relacyjnego jest zaledwie początkiem pracy. Stabilność aplikacji zależy w równej mierze od rygorystycznego zarządzania fizyczną strukturą [...]

Holistyczne spojrzenie na administrację PostgreSQL, obejmujące zarówno automatyzację procesów porządkujących pamięć, jak i ciągłe monitorowanie planów wykonania zapytań, pozwala na bu[...]
