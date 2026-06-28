================================================
Komunikacja i operacje na danych
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wstęp
=====

Po zdefiniowaniu znormalizowanego modelu logicznego i zasileniu struktur bazodanowych w poprzednich rozdziałach, system biblioteczny wymagał interfejsu zdolnego do obsługi zaawansowanej logiki biznesowej. Zamiast osadzać instrukcje SQL bezpośrednio w warstwie prezentacji, zaimplementowano dedykowaną warstwę dostępu do danych (*Data Access Layer*) w języku Python. Moduł ten zapewnia pełną abstrakcję, obsługując równolegle środowisko produkcyjne (PostgreSQL) oraz prototypowe (SQLite).

Wszystkie skrypty i zapytania zostały zaimplementowane, przetestowane oraz uruchomione w środowisku JupyterLab na serwerze laboratoryjnym. 

* **Katalog z funkcjami na serwerze:** ``/home/student15/lab/CLABC01/``
* **Repozytorium z kodem modułu:** `GitHub - Bazy-Danych-pliki <https://github.com/pawlos1337/Bazy-danych-pliki>`_

Zrezygnowano z trywialnych operacji CRUD na rzecz zapytań agregujących i analitycznych, które przenoszą ciężar obliczeniowy z aplikacji na silnik bazy danych. Wykorzystano zaawansowane techniki tworzenia rozbudowanych zapytań SQL, w tym:

* **Podzapytania (skorelowane i nieskorelowane):** Izolacja danych w klauzulach ``SELECT``, ``FROM`` i ``WHERE``, optymalizująca m.in. wielowarstwowe filtrowanie geolokalizacyjne w potężnych zbiorach danych.
* **Złączenia relacyjne (``JOIN``, ``LEFT JOIN``):** Wykorzystywane do łączenia rozproszonych danych transakcyjnych oraz detekcji asymetrii w systemie (np. precyzyjne wyłapywanie kategorii inwentarzowych bez przypisanych egzemplarzy).
* **Analizę agregacyjną (``GROUP BY``, ``HAVING``):** Generowanie kluczowych statystyk i identyfikacja trendów w obrocie zbiorami bibliotecznymi.
* **Operatory teorii mnogości (``UNION``, ``INTERSECT``, ``EXCEPT``):** Służące do wysokowydajnej, krzyżowej analizy preferencji czytelniczych, rozwiązywania problemu polimorfizmu encji (scalanie niezależnych tabel osób) oraz błyskawicznej identyfikacji pasywnych użytkowników.

Pełna specyfikacja stworzonego API
==================================

Zgodnie z dobrymi praktykami inżynierii oprogramowania, poniżej przedstawiono pełną, zautomatyzowaną specyfikację interfejsu programistycznego. Dokumentacja modułu obsługującego komunikację z bazami PostgreSQL oraz SQLite została wygenerowana bezpośrednio na podstawie komentarzy strukturalnych (Docstrings), w których dla pełnej przejrzystości zawarto również surowe kody zapytań SQL.

Zastosowanie mechanizmu kompilatora Sphinx gwarantuje absolutną zgodność dokumentacji ze stanem faktycznym implementacji w warstwie Python, eliminując problem z ręczną dezaktualizacją opisów.

.. automodule:: biblioteka_zapytania
   :members:
   :undoc-members:
   :show-inheritance:
