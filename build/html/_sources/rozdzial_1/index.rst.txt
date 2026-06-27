================
Wstęp oraz linki
================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wstęp do sprawozdania
=====================

Niniejsze sprawozdanie dokumentuje przebieg prac laboratoryjnych z przedmiotu Bazy Danych. Celem projektu jest praktyczne zastosowanie wiedzy z zakresu projektowania, wdrażania oraz obsługi systemów relacyjnych baz danych. 

Praca obejmuje pełen cykl życia bazy: od analizy teoretycznej systemów i zabezpieczeń, poprzez stworzenie modelu pojęciowego i logicznego, aż po fizyczną implementację w środowiskach PostgreSQL i SQLite. Proces ten dopełnia realizacja skryptów wsadowego zasilania danymi oraz komunikacja z bazą za pomocą dedykowanego interfejsu (Data Access Layer) w języku Python, w którym zaimplementowano zaawansowane, analityczne zapytania SQL.

Wnioski z przeprowadzonych ćwiczeń
==================================

Zrealizowane ćwiczenia laboratoryjne oraz eksperymenty programistyczne pozwoliły na wyciągnięcie następujących wniosków końcowych:

* **Kluczowa rola normalizacji:** Prawidłowo przeprowadzona normalizacja (do 3NF) na etapie projektowania logicznego skutecznie eliminuje redundancję danych oraz zapobiega powstawaniu anomalii podczas późniejszych operacji modyfikujących.
* **Różnice w silnikach bazodanowych:** Implementacja dwóch modeli fizycznych uwidoczniła przewagę PostgreSQL w rygorystycznym typowaniu i obsługi kluczy obcych nad elastyczniejszym, ale uboższym w natywne typy (np. brak formatu DATE) silnikiem SQLite.
* **Wydajność operacji wsadowych:** Wykorzystanie mechanizmów wprowadzania wielowartościowego (np. ``executemany()`` w Pythonie) jest fundamentalne dla skrócenia czasu zasilania relacyjnych baz danych w środowisku produkcyjnym, znacząco redukując narzut komunikacyjny (overhead).
* **Przenoszenie logiki do silnika bazy:** Zastosowanie zaawansowanych operatorów zbiorowych (UNION, INTERSECT), podzapytań oraz złączeń (JOIN) pozwala na optymalne wykonywanie operacji analitycznych bezpośrednio po stronie silnika bazy danych, zwalniając aplikację warstwy klienta z kosztownego przetwarzania struktur w pamięci RAM.

Wykaz repozytoriów (Linki)
==========================

Projekt został podzielony na odpowiednie repozytoria w systemie kontroli wersji Git, zapewniając porządek między dokumentacją a fizycznymi plikami środowiska bazodanowego.

1. Główne repozytorium sprawozdania (Dokumentacja Sphinx)
---------------------------------------------------------
Tutaj znajduje się struktura całej dokumentacji tekstowej, konfiguracja kompilatora Sphinx oraz historia zmian.

* **Link:** https://github.com/baguetedev/Bazy-Danych-1

2. Repozytorium z plikami projektowymi
--------------------------------------
W tym repozytorium umieszczono kody źródłowe, skrypty DDL dla silników PostgreSQL i SQLite, wygenerowany plik bazy oraz pliki CSV wykorzystywane do zasilania bazy danych.

* **Link WWW:** https://github.com/baguetedev/Bazy-Danych-pliki
* **Klonowanie SSH:** ``git@github.com:baguetedev/Bazy-Danych-pliki.git``

3. Repozytoria reszty grupy (Badania literaturowe)
--------------------------------------------------
Poniżej znajdują się odnośniki do repozytoriów reszty grupy, które zostały zintegrowane z niniejszym sprawozdaniem w postaci submodułów w Rozdziale 2:

* **Grupa 1 (rozdzial_1):** https://github.com/karaskamil/Sprzet-dla-bazy-danych.git
* **Grupa 2 (rozdzial_2):** https://github.com/Youarecheck/Bazy_Danych_Tematyczne_Repo_MK.git
* **Grupa 3 (rozdzial_3):** https://github.com/pawlos1337/Bazy-danych-temat.git
* **Grupa 4 (rozdzial_4):** https://github.com/OskarProgrammer/monitorowanie_i_diagnostyka.git
* **Grupa 5 (rozdzial_5):** https://github.com/KMachoK/Tematyczne.git
* **Grupa 6 (rozdzial_6):** https://github.com/domino0472/Partycjonowani-Danych
* **Grupa 7 (rozdzial_7):** https://github.com/oski486/BazyDanych-Subject.git
* **Grupa 8 (rozdzial_8):** https://github.com/Koko9077/Kopie-zapasowe-i-odzyskiwanie-danych.git
