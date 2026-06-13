================================================
Rozdział 5: Komunikacja i operacje na danych
================================================

:Autorzy:
    1. Paweł Łoćwin
    2. Paweł Łosowski

Wstęp
=====

Po zdefiniowaniu i zasileniu struktur bazodanowych w poprzednich rozdziałach, system wymaga 
interfejsu zdolnego do obsługi zaawansowanej logiki biznesowej biblioteki. W tym celu zaimplementowano 
warstwę dostępu do danych (Data Access Layer) w języku Python. 

Wykorzystano techniki tworzenia rozbudowanych zapytań SQL, w tym:
* Podzapytania (skorelowane i nieskorelowane w klauzulach ``SELECT``, ``FROM``, ``WHERE``).
* Złączenia relacyjne (``JOIN``, ``LEFT JOIN``).
* Analizę agregacyjną (``GROUP BY``, ``HAVING``).
* Operatory teorii mnogości (``UNION``, ``INTERSECT``, ``EXCEPT``).

Pełna specyfikacja stworzonego API
==================================

Poniżej przedstawiono zautomatyzowaną dokumentację modułu obsługującego połączenia z 
bazami PostgreSQL oraz SQLite, wygenerowaną na podstawie wbudowanych komentarzy (Docstrings).

.. automodule:: biblioteka_zapytania
   :members:
   :undoc-members:
   :show-inheritance:
